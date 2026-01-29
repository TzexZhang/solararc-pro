# 数据库管理脚本

本目录包含用于初始化数据库和插入测试数据的Python脚本。设计完全符合《需求设计文档》第四章的数据库设计规范。

## 🎯 重要设计决策

### 使用UUID作为主键

所有表的主键（id字段）均使用 **UUID (String/CHAR(36))** 类型，而非传统的Integer自增ID。

**优势**:
- ✅ **分布式友好**: 可以在多台服务器上生成唯一ID而无需协调
- ✅ **安全性**: UUID不会暴露数据量和增长模式
- ✅ **全局唯一**: 跨系统的数据集成更简单
- ✅ **无锁插入**: 避免自增ID的性能瓶颈

**实现**:
- 使用 `CHAR(36)` 存储UUID字符串
- SQLAlchemy模型中配置 `default=lambda: str(uuid.uuid4())` 自动生成
- 所有外键关系也使用UUID类型

**示例**:
```python
# 模型定义
id = Column(
    CHAR(36),
    primary_key=True,
    default=lambda: str(uuid.uuid4()),
    unique=True,
    nullable=False,
    comment="主键ID (UUID)"
)

# 外键定义
building_id = Column(
    CHAR(36),
    ForeignKey("buildings.id", ondelete="CASCADE"),
    nullable=False,
    comment="建筑ID (UUID)"
)
```

## 文件说明

- `init_db.py` - 数据库初始化脚本，用于创建数据库和表结构
- `insert_demo_data.py` - Demo数据插入脚本，用于向数据库插入测试数据
- `README.md` - 本说明文件

## 使用前准备

### 1. 配置数据库连接

确保 `backend/.env` 文件中配置了正确的数据库连接信息：

```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/solararc_pro?charset=utf8mb4
```

### 2. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

**重要依赖**:
- `sqlalchemy==2.0.23` - ORM框架
- `geoalchemy2==0.14.2` - 空间数据支持
- `pymysql==1.1.0` - MySQL驱动
- `shapely==2.0.2` - 空间几何计算
- `aiomysql` - 异步MySQL驱动（自动安装）

## 使用方法

### 方法1：作为模块运行（推荐）

在项目根目录下执行：

```bash
# 初始化数据库
python -m backend.database.init_db

# 插入demo数据
python -m backend.database.insert_demo_data

# 插入demo数据（清除现有数据）
python -m backend.database.insert_demo_data --clear
```

### 方法2：直接运行脚本

```bash
# 进入database目录
cd backend/database

# 初始化数据库
python init_db.py

# 插入demo数据
python insert_demo_data.py

# 插入demo数据（清除现有数据）
python insert_demo_data.py --clear
```

## 脚本功能说明

### init_db.py - 数据库初始化脚本

执行以下操作：
1. 创建数据库（如果不存在）
2. 创建所有数据表（符合需求文档§4.2节）
3. 创建空间索引
4. 验证表是否创建成功

**创建的数据表**（符合需求文档§4.2节）:
- `buildings` (§4.2.1) - 建筑信息表
- `solar_positions_precalc` (§4.2.2) - 太阳位置预计算表
- `shadow_analysis_cache` (§4.2.3) - 阴影分析缓存表
- `user_settings` (§4.2.4) - 用户配置表

### insert_demo_data.py - Demo数据插入脚本

执行以下操作：
1. 插入8个中国主要城市的超高层建筑数据
2. 为每个建筑创建多天的阴影分析缓存记录
3. 插入关键日期（春分、夏至、秋分、冬至）的太阳位置预计算数据

**包含的建筑**:
- 上海中心大厦（632m）
- 环球金融中心（492m）
- 金茂大厦（420.5m）
- 北京中信大厦（528m）
- 深圳平安国际金融中心（599.1m）
- 广州周大福金融中心（530m）
- 成都绿地中心（468m）
- 武汉绿地中心（475m）

命令行参数：
- `--clear` - 清除现有数据后再插入

## 数据库表结构

### 1. buildings 表 (需求文档§4.2.1)

建筑信息表，存储建筑的几何信息和元数据。

| 字段 | 类型 | 说明 | 参考 |
|------|------|------|------|
| id | CHAR(36) | 主键 (UUID) | 自动生成 |
| name | String(255) | 建筑名称 | - |
| building_type | String(50) | 建筑类型 (residential/commercial/industrial/public) | - |
| footprint | POLYGON | 建筑底面多边形 (WGS84, SRID 4326) | 空间索引 |
| total_height | Decimal(10,2) | 总高度(米) | - |
| floor_area | Decimal(15,2) | 楼层面积(平方米) | - |
| floor_count | Integer | 楼层数 | - |
| reflective_rate | Decimal(3,2) | 反射率(0-1) | - |
| address | String(500) | 地址 | - |
| district | String(100) | 区域 | - |
| city | String(100) | 城市 | - |
| country | String(50) | 国家 | - |
| created_at | DateTime | 创建时间 | - |
| updated_at | DateTime | 更新时间 | - |

**索引**:
- `PRIMARY KEY` (id)
- `SPATIAL INDEX idx_footprint` (footprint)

---

### 2. solar_positions_precalc 表 (需求文档§4.2.2)

太阳位置预计算表，用于优化关键日期的查询性能。

| 字段 | 类型 | 说明 | 参考 |
|------|------|------|------|
| id | CHAR(36) | 主键 (UUID) | 自动生成 |
| latitude | Decimal(10,6) | 纬度 | - |
| longitude | Decimal(10,6) | 经度 | - |
| date | Date | 日期 | - |
| hour | SmallInteger | 小时(0-23) | - |
| altitude_angle | Decimal(10,6) | 太阳高度角(度) | - |
| azimuth_angle | Decimal(10,6) | 太阳方位角(度) | - |
| created_at | DateTime | 创建时间 | - |

**索引**:
- `PRIMARY KEY` (id)
- `UNIQUE KEY idx_location_datetime` (latitude, longitude, date, hour)
- `INDEX idx_date` (date)

**说明**:
- 仅预计算关键日期: 春分、夏至、秋分、冬至
- 其他日期通过算法实时计算（使用pvlib）

---

### 3. shadow_analysis_cache 表 (需求文档§4.2.3)

阴影分析缓存表，用于缓存阴影计算结果，避免重复计算。

| 字段 | 类型 | 说明 | 参考 |
|------|------|------|------|
| id | CHAR(36) | 主键 (UUID) | 自动生成 |
| building_id | CHAR(36) | 建筑ID（外键UUID） | → buildings(id) |
| analysis_date | Date | 分析日期 | - |
| analysis_hour | SmallInteger | 分析小时(0-23) | - |
| shadow_polygon | POLYGON | 阴影多边形 (WGS84) | 空间索引 |
| shadow_area | Decimal(15,2) | 阴影面积(平方米) | - |
| created_at | DateTime | 创建时间 | - |
| expires_at | DateTime | 缓存过期时间 | - |

**索引**:
- `PRIMARY KEY` (id)
- `INDEX idx_building_datetime` (building_id, analysis_date, analysis_hour)
- `INDEX idx_expires` (expires_at)
- `SPATIAL INDEX idx_shadow_polygon` (shadow_polygon)

**外键**:
- `FOREIGN KEY (building_id) REFERENCES buildings(id) ON DELETE CASCADE`

---

### 4. user_settings 表 (需求文档§4.2.4)

用户配置表，用于存储前端会话的地图状态和分析参数。

| 字段 | 类型 | 说明 | 参考 |
|------|------|------|------|
| id | CHAR(36) | 主键 (UUID) | 自动生成 |
| session_id | String(128) | 前端会话ID | UNIQUE |
| map_center_lat | Decimal(10,6) | 地图中心纬度 | - |
| map_center_lng | Decimal(10,6) | 地图中心经度 | - |
| map_zoom | SmallInteger | 地图缩放级别 | - |
| analysis_date | Date | 分析日期 | - |
| current_hour | SmallInteger | 当前分析小时(0-23) | - |
| updated_at | DateTime | 更新时间 | - |

**索引**:
- `PRIMARY KEY` (id)
- `UNIQUE KEY idx_session` (session_id)

---

## 空间数据支持

### 坐标系系统

项目使用 **WGS84** 坐标系 (SRID 4326)，符合GPS标准。

**中国坐标系支持** (需求文档§1.4.1):
- WGS84 - 全球标准坐标系（GPS原始坐标）
- GCJ-02 - 国测局坐标系（高德、腾讯地图）
- BD-09 - 百度坐标系

坐标转换功能由 `app/services/coord_system.py` 提供。

### 空间索引

MySQL的空间索引用于加速空间查询：

```sql
-- 建筑底面空间索引
CREATE SPATIAL INDEX idx_footprint ON buildings(footprint);

-- 阴影多边形空间索引
CREATE SPATIAL INDEX idx_shadow_polygon ON shadow_analysis_cache(shadow_polygon);
```

### Bounding Box查询

仅查询视野范围内的建筑：

```sql
SELECT * FROM buildings
WHERE MBRContains(
    ST_GeomFromText(
        'POLYGON((min_lng min_lat, max_lng min_lat, max_lng max_lat, min_lng max_lat, min_lng min_lat))',
        4326
    ),
    footprint
);
```

## 数据库优化策略

### 1. 预计算优化 (需求文档§4.3.1)

**太阳位置预计算**:
- 仅预计算关键日期（春分、夏至、秋分、冬至）
- 其他日期实时计算
- 使用 pvlib 的 `solarposition.get_solarposition()` 函数

### 2. 缓存策略 (需求文档§4.3.2)

**阴影分析缓存**:
- 缓存有效期：7天
- 自动清理过期数据
- 支持手动清除缓存

### 3. 查询优化 (需求文档§4.3.3)

**Bounding Box查询**:
- 仅加载视野范围内的建筑
- 减少数据传输量
- 提升前端渲染性能

## 注意事项

1. **空间数据格式**: 使用 WKT (Well-Known Text) 格式插入空间数据
2. **SRID指定**: 所有空间数据必须指定 SRID 4326 (WGS84)
3. **数据备份**: 在生产环境使用前，请先备份重要数据
4. **权限要求**: 确保数据库用户有创建数据库、表和索引的权限
5. **字符编码**: 数据库使用 utf8mb4 字符集，支持emoji等特殊字符
6. **--clear参数**: 使用 `--clear` 参数会删除所有现有数据，请谨慎使用

## 故障排除

### 1. 连接数据库失败

**症状**: `Can't connect to MySQL server`

**解决方案**:
```bash
# 确保MySQL服务正在运行
# Windows
net start MySQL

# Linux/Mac
sudo systemctl start mysql
# 或
sudo service mysql start
```

### 2. 空间数据插入失败

**症状**: `Invalid geometry data`

**解决方案**:
- 确保WKT格式正确
- 确保多边形是闭合的（首尾坐标相同）
- 确保坐标顺序正确（经度在前，纬度在后）

```python
from geoalchemy2 import WKTElement

# 正确的WKT格式
footprint = WKTElement(
    'POLYGON((lng1 lat1, lng2 lat2, lng3 lat3, lng1 lat1))',
    srid=4326
)
```

### 3. 空间索引创建失败

**症状**: `Can't create table`

**解决方案**:
```sql
-- 检查MySQL是否支持空间索引
SHOW VARIABLES LIKE 'have_geometry%';

-- 应该显示：
-- have_geometry = YES
-- have_rtree_keys = YES (MySQL 5.7.5+)
```

### 4. 模块导入错误

**症状**: `ModuleNotFoundError: No module named 'app'`

**解决方案**:
- 确保在项目根目录下执行命令
- 确保Python路径包含项目根目录
- 检查虚拟环境是否激活

## 开发建议

### 1. 本地开发

```bash
# 1. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 安装依赖
pip install -r backend/requirements.txt

# 3. 初始化数据库
python -m backend.database.init_db

# 4. 插入测试数据
python -m backend.database.insert_demo_data

# 5. 启动后端服务
cd backend
uvicorn main:app --reload --port 8000
```

### 2. 数据清理

定期清理过期缓存：

```sql
-- 删除过期的阴影分析缓存
DELETE FROM shadow_analysis_cache
WHERE expires_at < NOW();
```

### 3. 性能监控

```sql
-- 查看表大小
SELECT
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.TABLES
WHERE table_schema = 'solararc_pro'
ORDER BY (data_length + index_length) DESC;

-- 查看索引使用情况
SHOW INDEX FROM buildings;
SHOW INDEX FROM shadow_analysis_cache;
```

## 需求文档对照

本数据库设计完全符合《需求设计文档》第四章的要求：

| 需求章节 | 表名 | 状态 |
|---------|------|------|
| §4.2.1 | buildings | ✅ 完成 |
| §4.2.2 | solar_positions_precalc | ✅ 完成 |
| §4.2.3 | shadow_analysis_cache | ✅ 完成 |
| §4.2.4 | user_settings | ✅ 完成 |
| §4.3.1 | 空间索引 | ✅ 完成 |
| §4.3.2 | 预计算优化 | ✅ 完成 |
| §4.3.3 | Bounding Box查询 | ✅ 支持 |

## 更多信息

- 需求文档: `docs/需求设计文档.md`
- API文档: 待补充
- 部署指南: `docs/部署指南.md` (待创建)

---

**维护者**: SolarArc Pro 开发团队
**更新日期**: 2026-01-29
**版本**: v1.1
