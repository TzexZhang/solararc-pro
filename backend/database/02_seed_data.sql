-- SolarArc Pro Demo Data
-- 插入测试用户和示例建筑数据
-- Encoding: UTF-8MB4

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- 0. 清空现有数据（避免重复键错误）
-- ============================================
TRUNCATE TABLE building_scores;
TRUNCATE TABLE analysis_reports;
TRUNCATE TABLE projects;
TRUNCATE TABLE shadow_analysis_cache;
TRUNCATE TABLE solar_positions_precalc;
TRUNCATE TABLE buildings;
TRUNCATE TABLE password_resets;
TRUNCATE TABLE users;

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================
-- 1. 插入测试用户
-- ============================================
INSERT INTO users (id, email, password_hash, nickname, is_active) VALUES
('550e8400-e29b-41d4-a716-446655440000',
 'admin@solararc.pro',
 '$2b$12$LQv3c1yqBWVHxkd0LHAkJbK3OpfbGC7Q.CjZXIoQKEBjTbN6c9yNU9q0C5q9HqW8',
 '系统管理员',
 TRUE);

INSERT INTO users (id, email, password_hash, nickname, is_active) VALUES
('550e8400-e29b-41d4-a716-446655440001',
 'demo@solararc.pro',
 '$2b$12$LQv3c1yqBWVHxkd0LHAkJbK3OpfbGC7Q.CjZXIoQKEBjTbN6c9yNU9q0C5q9HqW8',
 '演示用户',
 TRUE);

INSERT INTO users (id, email, password_hash, nickname, is_active) VALUES
('550e8400-e29b-41d4-a716-446655440002',
 'test@solararc.pro',
 '$2b$12$LQv3c1yqBWVHxkd0LHAkJbK3OpfbGC7Q.CjZXIoQKEBjTbN6c9yNU9q0C5q9HqW8',
 '测试用户',
 TRUE);

-- 默认密码都是：password123
-- 以上哈希值对应密码 "password123"

-- ============================================
-- 2. 插入示例建筑数据（北京市朝阳区示例）
-- ============================================
INSERT INTO buildings (id, name, building_type, footprint, total_height, floor_area, floor_count, city, district, address) VALUES
-- 示例建筑1：高层办公楼
('550e8400-e29b-41d4-a716-446655440010',
 '国贸大厦A座',
 'commercial',
 ST_GeomFromText('POLYGON((39.9050 116.4567, 39.9050 116.4580, 39.9070 116.4580, 39.9070 116.4567, 39.9050 116.4567))', 4326),
 155.5,
 85000.50,
 35,
 '北京',
 '朝阳区',
 '北京市朝阳区建国门外大街1号'),

-- 示例建筑2：住宅楼
('550e8400-e29b-41d4-a716-446655440011',
 '阳光花园3号楼',
 'residential',
 ST_GeomFromText('POLYGON((39.9020 116.4590, 39.9020 116.4615, 39.9040 116.4615, 39.9040 116.4590, 39.9020 116.4590))', 4326),
 78.0,
 12500.0,
 26,
 '北京',
 '朝阳区',
 '北京市朝阳区望京街道阜通东大街'),

-- 示例建筑3：商业中心
('550e8400-e29b-41d4-a716-446655440012',
 'SOHO现代城',
 'commercial',
 ST_GeomFromText('POLYGON((39.9000 116.4620, 39.9000 116.4645, 39.9020 116.4645, 39.9020 116.4620, 39.9000 116.4620))', 4326),
 105.0,
 42000.0,
 22,
 '北京',
 '朝阳区',
 '北京市朝阳区建外SOHO区'),

-- 示例建筑4：公共设施
('550e8400-e29b-41d4-a716-446655440013',
 '朝阳公园艺术中心',
 'public',
 ST_GeomFromText('POLYGON((39.9100 116.4700, 39.9100 116.4725, 39.9120 116.4725, 39.9120 116.4700, 39.9100 116.4700))', 4326),
 25.0,
 8000.0,
 5,
 '北京',
 '朝阳区',
 '北京市朝阳区朝阳公园南路'),

-- 示例建筑5：工业建筑
('550e8400-e29b-41d4-a716-446655440014',
 '科技研发中心',
 'industrial',
 ST_GeomFromText('POLYGON((39.9150 116.4500, 39.9150 116.4525, 39.9170 116.4525, 39.9170 116.4500, 39.9150 116.4500))', 4326),
 45.0,
 15000.0,
 10,
 '北京',
 '朝阳区',
 '北京市朝阳区科技园'),

-- 示例建筑6：住宅小区
('550e8400-e29b-41d4-a716-446655440015',
 '万科金域蓝湾',
 'residential',
 ST_GeomFromText('POLYGON((39.8950 116.4650, 39.8950 116.4675, 39.8970 116.4675, 39.8970 116.4650, 39.8950 116.4650))', 4326),
 88.0,
 22000.0,
 28,
 '北京',
 '朝阳区',
 '北京市朝阳区东坝乡'),

-- 示例建筑7：商业综合体
('550e8400-e29b-41d4-a716-446655440016',
 '华贸购物中心',
 'commercial',
 ST_GeomFromText('POLYGON((39.9080 116.4680, 39.9080 116.4705, 39.9100 116.4705, 39.9100 116.4680, 39.9080 116.4680))', 4326),
 135.0,
 65000.0,
 32,
 '北京',
 '朝阳区',
 '北京市朝阳区华贸中心'),

-- 示例建筑8：住宅小区
('550e8400-e29b-41d4-a716-446655440017',
 '天鹅湾畔',
 'residential',
 ST_GeomFromText('POLYGON((39.9200 116.4720, 39.9200 116.4745, 39.9220 116.4745, 39.9220 116.4720, 39.9200 116.4720))', 4326),
 95.0,
 18000.0,
 30,
 '北京',
 '朝阳区',
 '北京市朝阳区天鹅湾小区');

-- ============================================
-- 3. 插入示例项目
-- ============================================
INSERT INTO projects (id, user_id, name, description, center_latitude, center_longitude, zoom_level, config) VALUES
('550e8400-e29b-41d4-a716-446655440020',
 '550e8400-e29b-41d4-a716-446655440000',
 '北京朝阳区日照分析项目',
 '分析朝阳区主要建筑的日照情况，包含8个典型建筑',
 39.9080,
 116.4630,
 15,
  '{"map_style": "light", "show_shadows": true, "animation_speed": 1.0}'),

('550e8400-e29b-41d4-a716-446655440021',
 '550e8400-e29b-41d4-a716-446655440001',
 'CBD核心区建筑群分析',
 '分析CBD核心区商业建筑的日照影响',
 39.9070,
 116.4600,
 16,
 '{"map_style": "dark", "show_shadows": true, "animation_enabled": true}');

-- ============================================
-- 4. 插入示例太阳位置数据（北京位置，关键日期）
-- ============================================
-- 北京坐标：纬度 39.9042, 经度 116.4074
-- 日期：2024-06-21 (夏至) 和 2024-12-22 (冬至)

-- 夏至日太阳位置数据（每2小时一个点）
INSERT INTO solar_positions_precalc (id, latitude, longitude, date, hour, altitude_angle, azimuth_angle) VALUES
-- 夏至日
('550e8400-e29b-41d4-a716-4466554030', 39.9042, 116.4074, '2024-06-21', 4, -20.5, 65.2),
('550e8400-e29b-41d4-a716-4466554031', 39.9042, 116.4074, '2024-06-21', 6, -10.3, 72.5),
('550e8400-e29b-41d4-a716-4466554032', 39.9042, 116.4074, '2024-06-21', 8, 15.8, 82.3),
('550e8400-e29b-41d4-a716-4466554033', 39.9042, 116.4074, '2024-06-21', 10, 35.6, 95.8),
('550e8400-e29b-41d4-a716-4466554034', 39.9042, 116.4074, '2024-06-21', 12, 73.5, 180.2),
('550e8400-e29b-41d4-a716-4466554035', 39.9042, 116.4074, '2024-06-21', 14, 65.4, 254.6),
('550e8400-e29b-41d4-a716-4466554036', 39.9042, 116.4074, '2024-06-21', 16, 42.1, 285.3),
('550e8400-e29b-41d4-a716-4466554037', 39.9042, 116.4074, '2024-06-21', 18, 15.6, 305.8),
('550e8400-e29b-41d4-a716-4466554038', 39.9042, 116.4074, '2024-06-21', 20, -10.3, 324.2),

-- 冬至日
('550e8400-e29b-41d4-a716-4466554039', 39.9042, 116.4074, '2024-12-22', 4, -60.5, 62.8),
('550e8400-e29b-41d4-a716-4466554040', 39.9042, 116.4074, '2024-12-22', 6, -50.3, 70.5),
('550e8400-e29b-41d4-a716-4466554041', 39.9042, 116.4074, '2024-12-22', 8, -35.2, 85.3),
('550e8400-e29b-41d4-a716-4466554042', 39.9042, 116.4074, '2024-12-22', 10, -15.6, 115.2),
('550e8400-e29b-41d4-a716-4466554043', 39.9042, 116.4074, '2024-12-22', 12, 26.8, 180.5),
('550e8400-e29b-41d4-a716-4466554044', 39.9042, 116.4074, '2024-12-22', 14, 32.1, 210.8),
('550e8400-e29b-41d4-a716-4466554045', 39.9042, 116.4074, '2024-12-22', 16, 25.4, 265.3),
('550e8400-e29b-41d4-a716-4466554046', 39.9042, 116.4074, '2024-12-22', 18, 10.3, 285.6),
('550e8400-e29b-41d4-a716-4466554047', 39.9042, 116.4074, '2024-12-22', 20, -20.5, 304.2);

-- ============================================
-- 5. 插入示例分析报告
-- ============================================
INSERT INTO analysis_reports (
    id,
    user_id,
    project_id,
    name,
    analysis_type,
    latitude,
    longitude,
    date_start,
    date_end,
    total_sunlight_hours,
    avg_shadow_coverage,
    building_count,
    results,
    created_at,
    updated_at
) VALUES (
    '550e8400-e29b-41d4-a716-446655440050',
    '550e8400-e29b-41d4-a716-446655440000',
    '550e8400-e29b-41d4-a716-446655440020',
    '2024年夏至日照分析报告',
    'daily',
    39.9080,
    116.4630,
    '2024-06-21',
    '2024-06-21',
    1250.5,
    35.2,
    8,
    '{"hourly_sunlight": [0,0,0,0,0.5,2.5,5.8,8.5,11.2,13.5,15.0,15.8,15.5,14.8,12.5,9.8,7.2,5.0,3.2,1.8,0.5,0,0,0,0,0,0,0,0,0,0,0], "building_scores": [{"building_id": "550e8400-e29b-41d4-a716-446655440010", "avg_sunlight_hours": 8.5, "grade": "excellent"}, {"building_id": "550e8400-e29b-41d4-a716-446655440011", "avg_sunlight_hours": 7.2, "grade": "good"}]}',
    NOW(),
    NOW()
);

-- ============================================
-- 6. 插入建筑采光评分
-- ============================================
INSERT INTO building_scores (
    id,
    report_id,
    building_id,
    overall_score,
    grade,
    avg_sunlight_hours,
    peak_sunlight_hours,
    continuous_sunlight_hours,
    shadow_frequency,
    shading_buildings
) VALUES
(
    '550e8400-e29b-41d4-a716-4466554060',
    '550e8400-e29b-41d4-a716-446655440050',
    '550e8400-e29b-41d4-a716-446655440010',
    85,
    'excellent',
    8.5,
    12.0,
    6.0,
    2,
    '["550e8400-e29b-41d4-a716-446655440011"]'
),
(
    '550e8400-e29b-41d4-a716-4466554061',
    '550e8400-e29b-41d4-a716-446655440050',
    '550e8400-e29b-41d4-a716-446655440011',
    72,
    'good',
    7.2,
    10.5,
    5.0,
    3,
    '["550e8400-e29b-41d4-a716-446655440010"]'
);

SELECT 'Demo data inserted successfully!' as message;
SELECT '====================================' as message;
SELECT 'Demo Users:' as info;
SELECT email AS 'Email', nickname AS 'Nickname' FROM users;
SELECT '====================================' as message;
SELECT 'Demo Buildings:' as info;
SELECT name AS 'Building Name', building_type AS 'Type', total_height AS 'Height(m)' FROM buildings;
SELECT '====================================' as message;
SELECT 'Demo Projects:' as info;
SELECT name AS 'Project Name' FROM projects;
SELECT '====================================' as message;
SELECT 'Demo Reports:' as info;
SELECT name AS 'Report Name', analysis_type AS 'Type' FROM analysis_reports;
