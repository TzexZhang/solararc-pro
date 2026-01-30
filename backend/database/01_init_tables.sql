-- SolarArc Pro Database Initialization Script
-- MySQL 8.0+
-- Encoding: UTF-8MB4

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- 1. 用户表
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY COMMENT '用户ID（UUID）',
    email VARCHAR(255) UNIQUE NOT NULL COMMENT '邮箱（登录账号）',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希（bcrypt）',
    nickname VARCHAR(50) COMMENT '用户昵称',

    -- 账户状态
    is_active BOOLEAN DEFAULT TRUE COMMENT '账户是否激活',
    is_locked BOOLEAN DEFAULT FALSE COMMENT '账户是否锁定',
    failed_login_count INT DEFAULT 0 COMMENT '失败登录次数',
    locked_until DATETIME COMMENT '锁定到期时间',

    -- 登录信息
    last_login_at TIMESTAMP NULL COMMENT '最后登录时间',
    last_login_ip VARCHAR(45) COMMENT '最后登录IP',

    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- 索引
    INDEX idx_email (email),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- ============================================
-- 2. 密码重置表
-- ============================================
CREATE TABLE IF NOT EXISTS password_resets (
    id VARCHAR(36) PRIMARY KEY COMMENT '重置ID（UUID）',
    user_id VARCHAR(36) NOT NULL COMMENT '用户ID',
    token VARCHAR(255) UNIQUE NOT NULL COMMENT '重置令牌',
    expires_at DATETIME NOT NULL COMMENT '过期时间',
    used BOOLEAN DEFAULT FALSE COMMENT '是否已使用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 外键
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,

    -- 索引
    INDEX idx_user_id (user_id),
    INDEX idx_expires_at (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='密码重置表';

-- ============================================
-- 3. 建筑表
-- ============================================
CREATE TABLE IF NOT EXISTS buildings (
    id VARCHAR(36) PRIMARY KEY COMMENT '建筑ID（UUID）',
    name VARCHAR(255) COMMENT '建筑名称',
    building_type ENUM('residential', 'commercial', 'industrial', 'public') COMMENT '建筑类型',

    -- 空间几何数据
    footprint POLYGON NOT NULL SRID 4326 COMMENT '建筑底面多边形 (WGS84)',
    total_height DECIMAL(10, 2) NOT NULL COMMENT '总高度(米)',
    floor_area DECIMAL(15, 2) COMMENT '楼层面积(平方米)',
    floor_count INT COMMENT '楼层数',

    -- 光学属性
    reflective_rate DECIMAL(3, 2) DEFAULT 0.3 COMMENT '反射率(0-1)',

    -- 元数据
    address VARCHAR(500),
    district VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(50) DEFAULT 'China',

    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- 空间索引
    SPATIAL INDEX idx_footprint (footprint)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='建筑信息表';

-- ============================================
-- 4. 太阳位置预计算表
-- ============================================
CREATE TABLE IF NOT EXISTS solar_positions_precalc (
    id VARCHAR(36) PRIMARY KEY COMMENT '记录ID（UUID）',

    -- 位置参数
    latitude DECIMAL(10, 6) NOT NULL COMMENT '纬度',
    longitude DECIMAL(10, 6) NOT NULL COMMENT '经度',

    -- 时间参数
    date DATE NOT NULL COMMENT '日期',
    hour TINYINT NOT NULL COMMENT '小时(0-23)',

    -- 太阳位置参数
    altitude_angle DECIMAL(10, 6) NOT NULL COMMENT '太阳高度角(度)',
    azimuth_angle DECIMAL(10, 6) NOT NULL COMMENT '太阳方位角(度)',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 索引
    UNIQUE KEY idx_location_datetime (latitude, longitude, date, hour),
    INDEX idx_date (date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='太阳位置预计算表';

-- ============================================
-- 5. 阴影分析缓存表
-- ============================================
CREATE TABLE IF NOT EXISTS shadow_analysis_cache (
    id VARCHAR(36) PRIMARY KEY COMMENT '缓存ID（UUID）',

    -- 分析参数
    building_id VARCHAR(36) NOT NULL,
    analysis_date DATE NOT NULL,
    analysis_hour TINYINT NOT NULL,

    -- 计算结果 (存储为GeoJSON)
    shadow_polygon POLYGON NOT NULL SRID 4326 COMMENT '阴影多边形',
    shadow_area DECIMAL(15, 2) COMMENT '阴影面积(平方米)',

    -- 缓存元数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL COMMENT '缓存过期时间',

    -- 外键
    FOREIGN KEY (building_id) REFERENCES buildings(id) ON DELETE CASCADE,

    -- 索引
    INDEX idx_building_datetime (building_id, analysis_date, analysis_hour),
    INDEX idx_expires (expires_at),
    SPATIAL INDEX idx_shadow (shadow_polygon)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='阴影分析缓存表';

-- ============================================
-- 6. 项目表
-- ============================================
CREATE TABLE IF NOT EXISTS projects (
    id VARCHAR(36) PRIMARY KEY COMMENT '项目ID（UUID）',
    user_id VARCHAR(36) NOT NULL COMMENT '用户ID',
    name VARCHAR(255) NOT NULL COMMENT '项目名称',
    description TEXT COMMENT '项目描述',
    center_latitude DECIMAL(10, 7) NOT NULL COMMENT '中心纬度',
    center_longitude DECIMAL(10, 7) NOT NULL COMMENT '中心经度',
    zoom_level INT DEFAULT 15 COMMENT '缩放级别',
    config JSON COMMENT '配置参数',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- 外键
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,

    -- 索引
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户项目表';

-- ============================================
-- 7. 分析报告表
-- ============================================
CREATE TABLE IF NOT EXISTS analysis_reports (
    id VARCHAR(36) PRIMARY KEY COMMENT '报告ID（UUID）',
    user_id VARCHAR(36) NOT NULL COMMENT '用户ID',
    project_id VARCHAR(36) COMMENT '关联项目ID',
    name VARCHAR(255) NOT NULL COMMENT '报告名称',
    analysis_type ENUM('daily', 'seasonal', 'custom') NOT NULL COMMENT '分析类型',
    latitude DECIMAL(10, 7) NOT NULL COMMENT '分析中心纬度',
    longitude DECIMAL(10, 7) NOT NULL COMMENT '分析中心经度',
    date_start DATE NOT NULL COMMENT '分析开始日期',
    date_end DATE NOT NULL COMMENT '分析结束日期',
    total_sunlight_hours DECIMAL(10, 2) COMMENT '总日照时长',
    avg_shadow_coverage DECIMAL(5, 2) COMMENT '平均阴影覆盖率（%）',
    building_count INT COMMENT '分析建筑数量',
    results JSON NOT NULL COMMENT '详细分析结果（图表数据）',
    report_file_path VARCHAR(500) COMMENT 'PDF报告文件路径',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- 外键
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL,

    -- 索引
    INDEX idx_user_id (user_id),
    INDEX idx_project_id (project_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='分析报告表';

-- ============================================
-- 8. 建筑采光评分表
-- ============================================
CREATE TABLE IF NOT EXISTS building_scores (
    id VARCHAR(36) PRIMARY KEY COMMENT '评分ID（UUID）',
    report_id VARCHAR(36) NOT NULL COMMENT '关联报告ID',
    building_id VARCHAR(36) NOT NULL COMMENT '建筑ID',
    overall_score INT NOT NULL COMMENT '综合评分（0-100）',
    grade ENUM('excellent', 'good', 'moderate', 'poor') NOT NULL COMMENT '等级',
    avg_sunlight_hours DECIMAL(10, 2) COMMENT '平均日照时长',
    peak_sunlight_hours DECIMAL(10, 2) COMMENT '峰值日照时长',
    continuous_sunlight_hours DECIMAL(10, 2) COMMENT '最长连续日照时长',
    shadow_frequency INT COMMENT '被遮挡频次',
    shading_buildings JSON COMMENT '遮挡源建筑ID列表',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 外键
    FOREIGN KEY (report_id) REFERENCES analysis_reports(id) ON DELETE CASCADE,
    FOREIGN KEY (building_id) REFERENCES buildings(id) ON DELETE CASCADE,

    -- 索引
    INDEX idx_report_id (report_id),
    INDEX idx_building_id (building_id),
    INDEX idx_overall_score (overall_score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='建筑采光评分表';

-- ============================================
-- 9. 用户配置表
-- ============================================
CREATE TABLE IF NOT EXISTS user_settings (
    id VARCHAR(36) PRIMARY KEY COMMENT '配置ID（UUID）',
    session_id VARCHAR(128) NOT NULL COMMENT '前端会话ID',
    user_id VARCHAR(36) COMMENT '用户ID（关联用户，可选）',

    -- 地图状态
    map_center_lat DECIMAL(10, 6),
    map_center_lng DECIMAL(10, 6),
    map_zoom TINYINT,

    -- 分析参数
    analysis_date DATE,
    current_hour TINYINT,

    -- 时间戳
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- 外键
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,

    UNIQUE KEY idx_session (session_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户配置表';

-- ============================================
-- 完成初始化
-- ============================================
SET FOREIGN_KEY_CHECKS = 1;

SELECT 'Database tables created successfully!' as message;
