import React, { useState, useCallback, useRef } from 'react'
import { AutoComplete, message } from 'antd'
import { SearchOutlined } from '@ant-design/icons'
import { useMapStore } from '@/store'
import mapboxgl from 'mapbox-gl'
import { MAPBOX_ACCESS_TOKEN } from '@/config'
import './LocationSearch.css'

mapboxgl.accessToken = MAPBOX_ACCESS_TOKEN

// 扩展的中国城市列表（包含主要城市和地标）
const CITIES = [
  // 直辖市
  { value: '北京', label: '北京', lat: 39.9042, lng: 116.4074, zoom: 12 },
  { value: '上海', label: '上海', lat: 31.2304, lng: 121.4737, zoom: 12 },
  { value: '天津', label: '天津', lat: 39.0842, lng: 117.201, zoom: 12 },
  { value: '重庆', label: '重庆', lat: 29.4316, lng: 106.9123, zoom: 12 },

  // 省会城市
  { value: '广州', label: '广州', lat: 23.1291, lng: 113.2644, zoom: 12 },
  { value: '深圳', label: '深圳', lat: 22.5431, lng: 114.0579, zoom: 12 },
  { value: '杭州', label: '杭州', lat: 30.2741, lng: 120.1551, zoom: 12 },
  { value: '成都', label: '成都', lat: 30.5728, lng: 104.0668, zoom: 12 },
  { value: '武汉', label: '武汉', lat: 30.5928, lng: 114.3055, zoom: 12 },
  { value: '西安', label: '西安', lat: 34.3416, lng: 108.9398, zoom: 12 },
  { value: '南京', label: '南京', lat: 32.0603, lng: 118.7969, zoom: 12 },
  { value: '苏州', label: '苏州', lat: 31.2989, lng: 120.5853, zoom: 12 },
  { value: '长沙', label: '长沙', lat: 28.2282, lng: 112.9388, zoom: 12 },
  { value: '郑州', label: '郑州', lat: 34.7466, lng: 113.6253, zoom: 12 },
  { value: '沈阳', label: '沈阳', lat: 41.8057, lng: 123.4315, zoom: 12 },
  { value: '青岛', label: '青岛', lat: 36.0671, lng: 120.3826, zoom: 12 },
  { value: '大连', label: '大连', lat: 38.914, lng: 121.6147, zoom: 12 },
  { value: '厦门', label: '厦门', lat: 24.4798, lng: 118.0894, zoom: 12 },
  { value: '济南', label: '济南', lat: 36.6512, lng: 117.1201, zoom: 12 },
  { value: '哈尔滨', label: '哈尔滨', lat: 45.8038, lng: 126.534, zoom: 12 },
  { value: '长春', label: '长春', lat: 43.8171, lng: 125.3235, zoom: 12 },
  { value: '石家庄', label: '石家庄', lat: 38.0428, lng: 114.5149, zoom: 12 },
  { value: '太原', label: '太原', lat: 37.8706, lng: 112.5489, zoom: 12 },
  { value: '合肥', label: '合肥', lat: 31.8206, lng: 117.2272, zoom: 12 },
  { value: '南昌', label: '南昌', lat: 28.682, lng: 115.8579, zoom: 12 },
  { value: '福州', label: '福州', lat: 26.0745, lng: 119.2965, zoom: 12 },
  { value: '南宁', label: '南宁', lat: 22.817, lng: 108.3665, zoom: 12 },
  { value: '昆明', label: '昆明', lat: 25.0406, lng: 102.7129, zoom: 12 },
  { value: '贵阳', label: '贵阳', lat: 26.647, lng: 106.6302, zoom: 12 },
  { value: '兰州', label: '兰州', lat: 36.0611, lng: 103.8343, zoom: 12 },
  { value: '西宁', label: '西宁', lat: 36.6171, lng: 101.7782, zoom: 12 },
  { value: '银川', label: '银川', lat: 38.4872, lng: 106.2309, zoom: 12 },
  { value: '乌鲁木齐', label: '乌鲁木齐', lat: 43.8256, lng: 87.6168, zoom: 12 },
  { value: '拉萨', label: '拉萨', lat: 29.6525, lng: 91.1721, zoom: 12 },
  { value: '呼和浩特', label: '呼和浩特', lat: 40.8414, lng: 111.7519, zoom: 12 },
  { value: '海口', label: '海口', lat: 20.0174, lng: 110.3492, zoom: 12 },
  { value: '三亚', label: '三亚', lat: 18.2524, lng: 109.5117, zoom: 12 },
  { value: '温州', label: '温州', lat: 28.0002, lng: 120.6719, zoom: 12 },
  { value: '宁波', label: '宁波', lat: 29.8683, lng: 121.544, zoom: 12 },
  { value: '佛山', label: '佛山', lat: 23.0218, lng: 113.1219, zoom: 12 },
  { value: '东莞', label: '东莞', lat: 23.0205, lng: 113.7518, zoom: 12 },
  { value: '无锡', label: '无锡', lat: 31.4912, lng: 120.3119, zoom: 12 },
  { value: '常州', label: '常州', lat: 31.8106, lng: 119.9741, zoom: 12 },
  { value: '嘉兴', label: '嘉兴', lat: 30.7467, lng: 120.7506, zoom: 12 },
  { value: '绍兴', label: '绍兴', lat: 30.0299, lng: 120.5802, zoom: 12 },
  { value: '金华', label: '金华', lat: 29.0787, lng: 119.6479, zoom: 12 },
  { value: '台州', label: '台州', lat: 28.6563, lng: 121.4208, zoom: 12 },
  { value: '湖州', label: '湖州', lat: 30.8941, lng: 120.0867, zoom: 12 },
  { value: '丽水', label: '丽水', lat: 28.4675, lng: 119.9179, zoom: 12 },
  { value: '衢州', label: '衢州', lat: 28.9358, lng: 118.8597, zoom: 12 },
  { value: '舟山', label: '舟山', lat: 30.036, lng: 122.1064, zoom: 12 },
  { value: '珠海', label: '珠海', lat: 22.2769, lng: 113.5678, zoom: 12 },
  { value: '惠州', label: '惠州', lat: 23.1115, lng: 114.4152, zoom: 12 },
  { value: '中山', label: '中山', lat: 22.5171, lng: 113.3926, zoom: 12 },
  { value: '江门', label: '江门', lat: 22.5789, lng: 113.0816, zoom: 12 },
  { value: '肇庆', label: '肇庆', lat: 23.0469, lng: 112.4654, zoom: 12 },
  { value: '汕头', label: '汕头', lat: 23.3536, lng: 116.6819, zoom: 12 },
  { value: '湛江', label: '湛江', lat: 21.2708, lng: 110.3594, zoom: 12 },
  { value: '茂名', label: '茂名', lat: 21.6629, lng: 110.9252, zoom: 12 },
  { value: '韶关', label: '韶关', lat: 24.8108, lng: 113.5975, zoom: 12 },
  { value: '烟台', label: '烟台', lat: 37.4637, lng: 121.4479, zoom: 12 },
  { value: '潍坊', label: '潍坊', lat: 36.7067, lng: 119.1619, zoom: 12 },
  { value: '淄博', label: '淄博', lat: 36.8131, lng: 118.0548, zoom: 12 },
  { value: '威海', label: '威海', lat: 37.5131, lng: 122.1202, zoom: 12 },
  { value: '东营', label: '东营', lat: 37.4347, lng: 118.6751, zoom: 12 },
  { value: '泰安', label: '泰安', lat: 36.2003, lng: 117.0874, zoom: 12 },
  { value: '济宁', label: '济宁', lat: 35.4153, lng: 116.5871, zoom: 12 },
  { value: '临沂', label: '临沂', lat: 35.1041, lng: 118.3561, zoom: 12 },

  // 著名地标
  { value: '天安门', label: '天安门广场', lat: 39.9075, lng: 116.3972, zoom: 16 },
  { value: '故宫', label: '故宫博物院', lat: 39.9163, lng: 116.3971, zoom: 16 },
  { value: '外滩', label: '外滩', lat: 31.2396, lng: 121.4914, zoom: 16 },
  { value: '东方明珠', label: '东方明珠塔', lat: 31.2397, lng: 121.4998, zoom: 16 },
  { value: '西湖', label: '西湖', lat: 30.2475, lng: 120.1449, zoom: 15 },
  { value: '长城', label: '八达岭长城', lat: 40.3598, lng: 116.0163, zoom: 14 },
  { value: '颐和园', label: '颐和园', lat: 40.0011, lng: 116.2754, zoom: 15 },
  { value: '天坛', label: '天坛公园', lat: 39.8822, lng: 116.4103, zoom: 15 },
  { value: '圆明园', label: '圆明园', lat: 40.0087, lng: 116.2975, zoom: 15 },
  { value: '雍和宫', label: '雍和宫', lat: 39.9475, lng: 116.4187, zoom: 16 },
  { value: '布达拉宫', label: '布达拉宫', lat: 29.6577, lng: 91.1174, zoom: 16 },
  { value: '兵马俑', label: '兵马俑', lat: 34.3841, lng: 109.2785, zoom: 15 },
  { value: '大雁塔', label: '大雁塔', lat: 34.218, lng: 108.9647, zoom: 16 },
  { value: '黄鹤楼', label: '黄鹤楼', lat: 30.5446, lng: 114.3036, zoom: 16 },
  { value: '岳阳楼', label: '岳阳楼', lat: 29.3719, lng: 113.0955, zoom: 16 },
  { value: '滕王阁', label: '滕王阁', lat: 28.675, lng: 115.8914, zoom: 16 },
  { value: '蓬莱阁', label: '蓬莱阁', lat: 37.8493, lng: 120.7519, zoom: 16 },
  { value: '武侯祠', label: '武侯祠', lat: 30.6472, lng: 104.0435, zoom: 16 },
  { value: '杜甫草堂', label: '杜甫草堂', lat: 30.6589, lng: 104.0308, zoom: 16 },
  { value: '拙政园', label: '拙政园', lat: 31.3199, lng: 120.6283, zoom: 16 },
  { value: '留园', label: '留园', lat: 31.315, lng: 120.6017, zoom: 16 },
  { value: '网师园', label: '网师园', lat: 31.3196, lng: 120.6097, zoom: 16 },
  { value: '狮子林', label: '狮子林', lat: 31.3181, lng: 120.6192, zoom: 16 },
  { value: '虎丘', label: '虎丘', lat: 31.3393, lng: 120.5779, zoom: 15 },
  { value: '瘦西湖', label: '瘦西湖', lat: 32.3907, lng: 119.4212, zoom: 15 },
  { value: '个园', label: '个园', lat: 32.3924, lng: 119.4364, zoom: 16 },
  { value: '何园', label: '何园', lat: 32.3839, lng: 119.4386, zoom: 16 },
  { value: '鼓浪屿', label: '鼓浪屿', lat: 24.4466, lng: 118.0696, zoom: 15 },
  { value: '武夷山', label: '武夷山', lat: 27.738, lng: 117.9945, zoom: 13 },
  { value: '黄山', label: '黄山', lat: 30.1319, lng: 118.1666, zoom: 13 },
  { value: '泰山', label: '泰山', lat: 36.2577, lng: 117.1018, zoom: 14 },
  { value: '华山', label: '华山', lat: 34.4896, lng: 110.0889, zoom: 14 },
  { value: '衡山', label: '衡山', lat: 27.2742, lng: 112.6942, zoom: 14 },
  { value: '嵩山', label: '嵩山', lat: 34.4836, lng: 113.0235, zoom: 14 },
  { value: '峨眉山', label: '峨眉山', lat: 29.5423, lng: 103.4842, zoom: 14 },
  { value: '九寨沟', label: '九寨沟', lat: 33.1606, lng: 103.9169, zoom: 14 },
  { value: '张家界', label: '张家界', lat: 29.1167, lng: 110.4792, zoom: 14 },
  { value: '桂林', label: '桂林', lat: 25.2736, lng: 110.2901, zoom: 13 },
  { value: '阳朔', label: '阳朔', lat: 24.7796, lng: 110.4951, zoom: 14 },
  { value: '丽江', label: '丽江', lat: 26.8556, lng: 100.227, zoom: 14 },
  { value: '大理', label: '大理', lat: 25.6065, lng: 100.2678, zoom: 14 },
  { value: '香格里拉', label: '香格里拉', lat: 27.8193, lng: 99.7024, zoom: 14 },
  { value: '西双版纳', label: '西双版纳', lat: 22.0077, lng: 100.7979, zoom: 13 },
  { value: '三亚湾', label: '三亚湾', lat: 18.2533, lng: 109.4964, zoom: 14 },
  { value: '亚龙湾', label: '亚龙湾', lat: 18.206, lng: 109.6941, zoom: 15 },
  { value: '天涯海角', label: '天涯海角', lat: 18.2512, lng: 109.5126, zoom: 15 },
  { value: '蜈支洲岛', label: '蜈支洲岛', lat: 18.3149, lng: 109.7579, zoom: 15 },
  { value: '千岛湖', label: '千岛湖', lat: 29.6057, lng: 119.0379, zoom: 13 },
  { value: '青海湖', label: '青海湖', lat: 36.9694, lng: 100.1605, zoom: 11 },
  { value: '纳木错', label: '纳木错', lat: 30.7434, lng: 90.6036, zoom: 12 },
  { value: '呼伦贝尔', label: '呼伦贝尔', lat: 49.2122, lng: 119.7659, zoom: 10 },
  { value: '大兴安岭', label: '大兴安岭', lat: 51.6953, lng: 124.7126, zoom: 9 },
  { value: '长白山', label: '长白山', lat: 42.0086, lng: 128.0582, zoom: 11 },
  { value: '莫高窟', label: '莫高窟', lat: 40.0348, lng: 94.7859, zoom: 15 },
  { value: '月牙泉', label: '月牙泉', lat: 40.0843, lng: 94.6776, zoom: 15 },
  { value: '张掖丹霞', label: '张掖丹霞', lat: 38.9253, lng: 100.5264, zoom: 13 },
  { value: '茶卡盐湖', label: '茶卡盐湖', lat: 36.804, lng: 99.0758, zoom: 13 },
  { value: '可可西里', label: '可可西里', lat: 35.2415, lng: 91.0005, zoom: 10 },
  { value: '香港', label: '香港', lat: 22.3193, lng: 114.1694, zoom: 12 },
  { value: '澳门', label: '澳门', lat: 22.1987, lng: 113.5439, zoom: 13 },
  { value: '台北', label: '台北', lat: 25.033, lng: 121.5654, zoom: 12 },
  { value: '高雄', label: '高雄', lat: 22.6273, lng: 120.3014, zoom: 12 },
  { value: '台中', label: '台中', lat: 24.1477, lng: 120.6736, zoom: 12 },
  { value: '台南', label: '台南', lat: 22.9999, lng: 120.2269, zoom: 12 }
]

export const LocationSearch: React.FC = () => {
  const [searchValue, setSearchValue] = useState('')
  const [options, setOptions] = useState<
    { value: string; label: string; lat: number; lng: number; zoom: number }[]
  >([])
  const { setFlyToTarget } = useMapStore()

  // 搜索过滤
  const handleSearch = useCallback((value: string) => {
    if (!value) {
      setOptions([])
      return
    }

    const filtered = CITIES.filter(city => city.label.toLowerCase().includes(value.toLowerCase()))
    setOptions(filtered.slice(0, 10)) // 限制显示10个结果
  }, [])

  // 选择地点 - 使用飞行动效
  const handleSelect = useCallback(
    (value: string) => {
      const selected = options.find(opt => opt.value === value)
      if (selected) {
        console.log('选择地点:', selected.label, '坐标:', { lat: selected.lat, lng: selected.lng, zoom: selected.zoom })

        // 设置飞行目标，MapView会监听并执行飞行动效
        setFlyToTarget({
          latitude: selected.lat,
          longitude: selected.lng,
          zoom: selected.zoom
        })

        console.log('已设置flyToTarget')

        setSearchValue('')
        setOptions([])
        message.success(`已定位到：${selected.label}`)
      } else {
        console.warn('未找到选中的地点:', value)
        message.warning('未找到选中的地点')
      }
    },
    [options, setFlyToTarget]
  )

  return (
    <div className="location-search">
      <AutoComplete
        value={searchValue}
        options={options.map(opt => ({ value: opt.value, label: opt.label }))}
        onSearch={handleSearch}
        onSelect={handleSelect}
        onChange={setSearchValue}
        className="search-input"
        notFoundContent="未找到相关地点"
      >
        <div className="search-input-wrapper">
          <SearchOutlined className="search-icon" />
          <input
            className="search-input-field"
            placeholder="搜索城市或地点..."
            value={searchValue}
            onChange={e => setSearchValue(e.target.value)}
          />
          {searchValue && (
            <span className="search-clear" onClick={() => setSearchValue('')}>
              ×
            </span>
          )}
        </div>
      </AutoComplete>
    </div>
  )
}

export default LocationSearch
