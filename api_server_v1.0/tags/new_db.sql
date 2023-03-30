-- 生成删除所有表命令
-- SELECT CONCAT('DROP TABLE IF EXISTS ', table_name, ';')
-- FROM information_schema.`TABLES`
-- WHERE table_schema='new_crt';

-- 修改时区
set global time_zone = '+8:00';
FLUSH PRIVILEGES;
-- select now();
-- show variables like '%time_zone%';


DROP TABLE IF EXISTS tab_alarm_log;
DROP TABLE IF EXISTS tab_alarm_type;
DROP TABLE IF EXISTS tab_area;
DROP TABLE IF EXISTS tab_assign_device;
DROP TABLE IF EXISTS tab_build;
DROP TABLE IF EXISTS tab_center;
DROP TABLE IF EXISTS tab_controller;
DROP TABLE IF EXISTS tab_controller_op_log;
DROP TABLE IF EXISTS tab_device;
DROP TABLE IF EXISTS tab_device_type;
DROP TABLE IF EXISTS tab_floor;
DROP TABLE IF EXISTS tab_gb_evt_type;
DROP TABLE IF EXISTS tab_icon;
DROP TABLE IF EXISTS tab_maintenance_log;
DROP TABLE IF EXISTS tab_picture_type;
DROP TABLE IF EXISTS tab_project;
DROP TABLE IF EXISTS tab_project_picture;
DROP TABLE IF EXISTS tab_role;
DROP TABLE IF EXISTS tab_shift_record;
DROP TABLE IF EXISTS tab_system_log;
DROP TABLE IF EXISTS tab_system_param;
DROP TABLE IF EXISTS tab_user;
DROP TABLE IF EXISTS tab_version;



CREATE TABLE `tab_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `user_name` varchar(32) NOT NULL COMMENT '用户名',
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '密码',
  `role_id` int(11) NOT NULL COMMENT '角色id',
  `role_name` varchar(32) NOT NULL COMMENT '角色名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';



CREATE TABLE `tab_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `name` varchar(32) NOT NULL COMMENT '角色名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='权限表';



CREATE TABLE `tab_shift_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `watch_user_id` int(11) NOT NULL COMMENT '值班用户id',
  `watch_user_name` varchar(32) NOT NULL COMMENT '值班用户名',
  `change_user_id` int(11) NOT NULL COMMENT '换班用户id',
  `change_user_name` varchar(32) NOT NULL COMMENT '换班用户名',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='换班记录表';



CREATE TABLE `tab_system_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `snow_id` bigint DEFAULT NULL COMMENT '雪花id（19位）',
  `description` varchar(128) NOT NULL COMMENT '操作描述',
  `user_id` int(11) DEFAULT NULL COMMENT '用户id',
  `user_name` varchar(32) DEFAULT NULL COMMENT '用户名',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='系统操作记录表';



CREATE TABLE `tab_maintenance_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `description` varchar(128) NOT NULL COMMENT '维保描述',
  `operator_name` varchar(32) NOT NULL COMMENT '操作名称',
  `project_id` int(11) NOT NULL COMMENT '项目id',
  `user_id` int(11) NOT NULL COMMENT '维保人id',
  `user_name` varchar(32) NOT NULL COMMENT '维保人名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='维保记录';



CREATE TABLE `tab_picture_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `name` varchar(32) NOT NULL COMMENT '图片类型名称',
  `type` tinyint(1) NOT NULL COMMENT '文件分类（1 项目图片 2 楼宇图片 3 楼层图片 4 应急预案 5 控制室信息 6 其他）',
  `file_type` tinyint(1) NOT NULL DEFAULT '1' COMMENT '文件类型（1. 图片 2. pdf 3. word 4. xls）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='图片类型表';



CREATE TABLE `tab_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `name` varchar(128) NOT NULL COMMENT '项目名称',
  `address` varchar(128) NOT NULL COMMENT '项目地址',
  `mobile` varchar(32) DEFAULT NULL COMMENT '项目联系电话',
  `deploy_users` varchar(128) NOT NULL COMMENT '项目部署人员',  -- [{'id':1, 'name':'zhangsan'}]
  `is_active` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否为活跃项目（主项目）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='项目表';



CREATE TABLE `tab_project_picture` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `name` varchar(128) NOT NULL COMMENT '项目图片名称',
  `path` varchar(128) NOT NULL COMMENT '图片地址',
  `quick_svg_path` varchar(128) DEFAULT NULL COMMENT '图片地址（布点后生成的svg图片地址）',
  `picture_type_id` int(11) NOT NULL COMMENT '图片类型id',
  `picture_type_name` varchar(32) NOT NULL COMMENT '图片类型名称',
  `project_id` int(11) NOT NULL COMMENT '项目id',
  `is_home` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否为主页图片（0 否 1 是）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='项目图片信息表';



CREATE TABLE `tab_area` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `name` varchar(128) NOT NULL COMMENT '小区名称',
  `project_id` int(11) NOT NULL COMMENT '项目id',
  `project_name` varchar(32) NOT NULL COMMENT '项目名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='小区表';



CREATE TABLE `tab_build` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `name` varchar(32) NOT NULL COMMENT '楼宇名称',
  `path` varchar(128) NOT NULL COMMENT '图片地址',
  `picture_type_id` int(11) NOT NULL COMMENT '图片类型id',
  `picture_type_name` varchar(32) NOT NULL COMMENT '图片类型名称',
  `area_id` int(11) NOT NULL COMMENT '小区id',
  `area_name` varchar(32) NOT NULL COMMENT '小区名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='楼宇信息';



CREATE TABLE `tab_floor` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `name` varchar(32) NOT NULL COMMENT '楼层名称',
  `path` varchar(128) NOT NULL COMMENT '图片地址',
  `quick_svg_path` varchar(128) DEFAULT NULL COMMENT '图片地址（布点后生成的svg图片地址）',
  `picture_type_id` int(11) NOT NULL COMMENT '图片类型id',
  `picture_type_name` varchar(32) NOT NULL COMMENT '图片类型名称',
  `area_id` int(11) NOT NULL COMMENT '小区id',
  `area_name` varchar(32) NOT NULL COMMENT '小区名称',
  `build_id` int(11) NOT NULL COMMENT '楼宇id',
  `build_name` varchar(32) NOT NULL COMMENT '楼宇名称',
  `alarm` int(11) NOT NULL DEFAULT '0' COMMENT '报警总数',
  `fire` int(11) NOT NULL DEFAULT '0' COMMENT '火警数量',
  `malfunction` int(11) NOT NULL DEFAULT '0' COMMENT '故障数量',
  `vl_malfunction` int(11) NOT NULL DEFAULT '0' COMMENT '声光故障数量',
  `feedback` int(11) NOT NULL DEFAULT '0' COMMENT '反馈数量',
  `supervise` int(11) NOT NULL DEFAULT '0' COMMENT '监管数量',
  `shielding` int(11) NOT NULL DEFAULT '0' COMMENT '屏蔽数量',
  `vl_shielding` int(11) NOT NULL DEFAULT '0' COMMENT '声光屏蔽数量',
  `linkage` int(11) NOT NULL DEFAULT '0' COMMENT '联动数量',
  `inheritance_template` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否作为继承模板（0 否 1 是）',
  `inheritance` int(11) DEFAULT NULL COMMENT '继承（父级楼层id）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='楼层信息表';



CREATE TABLE `tab_controller` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `project_id` int(11) NOT NULL COMMENT '项目id',
  `project_name` varchar(32) NOT NULL COMMENT '项目名称',
  `name` varchar(32) NOT NULL COMMENT '控制器名称',
  `code` int(11) NOT NULL COMMENT '控制器号',
  `model` varchar(32) NOT NULL COMMENT '控制器版本',
  `manufacturer` varchar(32) NOT NULL COMMENT '制造商',
  `setup_date` date NOT NULL COMMENT '装机日期',
  `controller_type` tinyint(1) NOT NULL DEFAULT '2' COMMENT '控制器类型（1 主机 2 从机）',
  `host_id` int(11) DEFAULT NULL COMMENT '主机id',
  `is_online` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否在线（0 离线 1 在线）',
  `power_type` tinyint(1) NOT NULL DEFAULT '3' COMMENT '电源类型（1 主电 2 备电 3 未知）',
  `is_shielding` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否屏蔽 默认不屏蔽（0 否 1 是）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='控制器信息表';



CREATE TABLE `tab_controller_op_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `snow_id` bigint COMMENT '雪花id（19位）',
  `operate_time` datetime NOT NULL COMMENT '控制器操作时间',
  `controller_id` int(11) NOT NULL COMMENT '控制器id',
  `controller_num` int(11) NOT NULL COMMENT '控制器号',
  `controller_name` varchar(32) NOT NULL COMMENT '控制器名称',
  `gb_evt_type_id` int(11) NOT NULL COMMENT '国标事件类型id',
  `gb_evt_type_name` varchar(32) NOT NULL COMMENT '国标事件类型名称',
  `description` varchar(128) NOT NULL COMMENT '操作描述',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='控制器操作记录';



CREATE TABLE `tab_device_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `gb_device_type` varchar(32) NOT NULL COMMENT '国标码',
  `name` varchar(32) NOT NULL COMMENT '设备类型名称',
  `zx_device_type` int(11) NOT NULL COMMENT '内部编码（10进制）',
  `priority` int(11) NOT NULL COMMENT '优先级（用于查询时排序, 数字越小优先级越高）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='设备类型信息表';



CREATE TABLE `tab_icon` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `name` varchar(32) NOT NULL COMMENT '图标名称',
  `path` varchar(128) NOT NULL COMMENT '图标地址',
  `device_type_id` int(11) NOT NULL COMMENT '设备类型id',
  `device_type_name` varchar(32) NOT NULL COMMENT '设备类型名称',
  `gb_evt_type_id` int(11) DEFAULT NULL COMMENT '事件类型id',
  `gb_evt_type_name` varchar(32) DEFAULT NULL COMMENT '事件类型名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='设备图标表';



CREATE TABLE `tab_device` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `controller_id` int(11) NOT NULL COMMENT '控制器id',
  `controller_num` int(11) NOT NULL COMMENT '控制器号',
  `loop_num` int(11) DEFAULT NULL COMMENT '回路号',
  `addr_num` int(11) DEFAULT NULL COMMENT '地址号',
  `equipment_num` int(11) DEFAULT NULL COMMENT '设备号',
  `module_num` int(11) DEFAULT NULL COMMENT '模块号',
  `psn` varchar(32) NOT NULL COMMENT '设备编号',
  `manufacturer` varchar(32) NOT NULL COMMENT '制造商',
  `device_model` varchar(32) NOT NULL COMMENT '设备型号',
  `setup_date` date NOT NULL COMMENT '装机日期',
  `maintain_cycle` int(11) DEFAULT NULL COMMENT '维保周期',
  `expiration_date` date DEFAULT NULL COMMENT '有效期',
  `description` varchar(128) NOT NULL COMMENT '描述',
  `path` varchar(128) DEFAULT NULL COMMENT '设备图标地址',
  `is_online` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否在线（0 否 1 是）',
  `alarm` int(11) NOT NULL DEFAULT '0' COMMENT '报警总数',
  `fire` int(11) NOT NULL DEFAULT '0' COMMENT '火警数量',
  `malfunction` int(11) NOT NULL DEFAULT '0' COMMENT '故障数量',
  `vl_malfunction` int(11) NOT NULL DEFAULT '0' COMMENT '声光故障数量',
  `feedback` int(11) NOT NULL DEFAULT '0' COMMENT '反馈数量',
  `supervise` int(11) NOT NULL DEFAULT '0' COMMENT '监管数量',
  `shielding` int(11) NOT NULL DEFAULT '0' COMMENT '屏蔽数量',
  `vl_shielding` int(11) NOT NULL DEFAULT '0' COMMENT '声光屏蔽数量',
  `linkage` int(11) NOT NULL DEFAULT '0' COMMENT '联动数量',
  `is_assign` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否布点（0 否 1 是）',
  `assign_floor_id` int(11) DEFAULT NULL COMMENT '布点楼层id',
  `device_type_id` int(11) NOT NULL COMMENT '设备类型id',
  `device_type_name` varchar(32) NOT NULL COMMENT '设备类型名称',
  `device_type` tinyint(1) NOT NULL DEFAULT '1' COMMENT '设备类型（1 设备 2 控制器）',
  `area` varchar(32) DEFAULT NULL COMMENT '小区名称',
  `build` varchar(32) DEFAULT NULL COMMENT '楼宇名称',
  `unit` varchar(32) DEFAULT NULL COMMENT '单元名称',
  `floor` varchar(32) DEFAULT NULL COMMENT '楼层名称',
  `district` varchar(32) DEFAULT NULL COMMENT '分区名称',
  `room` varchar(32) DEFAULT NULL COMMENT '防烟分区名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='设备信息表';



CREATE TABLE `tab_assign_device` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `coordinate_X` double NOT NULL DEFAULT '0' COMMENT 'X轴坐标',
  `coordinate_Y` double NOT NULL DEFAULT '0' COMMENT 'Y轴坐标',
  `rate` double NOT NULL COMMENT '显示比例',
  `angle` int(11) DEFAULT '0' COMMENT '角度 默认为0',
  `width` double NOT NULL COMMENT '初始宽度',
  `height` double NOT NULL COMMENT '初始高度',
  `device_type_id` int(11) NOT NULL COMMENT '设备国标类型id',
  `device_type_name` varchar(32) NOT NULL COMMENT '设备国标类型名称',
  `path` varchar(128) NOT NULL COMMENT '图标地址',
  `description` varchar(128) NOT NULL COMMENT '描述',
  `device_status` int(11) DEFAULT 0 COMMENT '设备状态（0 正常 其他国标事件码）',
  `device_id` int(11) NOT NULL COMMENT '设备id',
  `psn` varchar(32) NOT NULL COMMENT '设备编号',
  `controller_num` int(11) NOT NULL COMMENT '控制器号',
  `loop_num` int(11) DEFAULT NULL COMMENT '回路号',
  `addr_num` int(11) DEFAULT NULL COMMENT '地址号',
  `equipment_num` int(11) DEFAULT NULL COMMENT '设备号',
  `module_num` int(11) DEFAULT NULL COMMENT '模块号',
  `floor_id` int(11) NOT NULL COMMENT '楼层id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='设备布点表';



CREATE TABLE `tab_alarm_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `name` varchar(32) NOT NULL COMMENT '报警类型名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='报警类型表';



CREATE TABLE `tab_alarm_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `is_clear` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否清除（已被清除的历史报警 0 否 1 是）',
  `snow_id` bigint NOT NULL COMMENT '雪花id（19位）',
  `alarm_time` datetime NOT NULL COMMENT '控制器报警时间',
  `description` varchar(128) NOT NULL COMMENT '报警描述',
  `controller_num` int(11) DEFAULT NULL COMMENT '控制器号',
  `loop_num` int(11) DEFAULT NULL COMMENT '回路号',
  `addr_num` int(11) DEFAULT NULL COMMENT '地址号',
  `equipment_num` int(11) DEFAULT NULL COMMENT '设备号',
  `module_num` int(11) DEFAULT NULL COMMENT '模块号',
  `pass_num` int(11) DEFAULT NULL COMMENT '通道号',
  `device_type_id` int(11) DEFAULT NULL COMMENT '设备类型id',
  `device_type_name` varchar(32) DEFAULT NULL COMMENT '设备类型名称',
  `area_id` int(11) DEFAULT NULL COMMENT '小区id',
  `area_name` varchar(32) DEFAULT NULL COMMENT '小区名称',
  `build_id` int(11) DEFAULT NULL COMMENT '楼宇id',
  `build_name` varchar(32) DEFAULT NULL COMMENT '楼宇名称',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id',
  `floor_name` varchar(32) DEFAULT NULL COMMENT '楼层名称',
  `device_id` int(11) DEFAULT NULL COMMENT '报警设备id',
  `alarm_type_id` int(11) NOT NULL COMMENT '报警类型id',
  `alarm_type_name` varchar(32) NOT NULL COMMENT '报警类型名称',
  `assign_status` tinyint(1) DEFAULT '0' COMMENT '布点状态（0 未布点 1 已布点）',
  `alarm_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '报警状态 （0消失 1出现 2丢弃）',
  `gb_evt_type_id` int(11) DEFAULT NULL COMMENT '事件国标类型id',
  `gb_evt_type_name` varchar(32) DEFAULT NULL COMMENT '事件国标类型名称',
  `alarm_type` tinyint(1) DEFAULT NULL COMMENT '报警类型（0 真实报警 1 模拟报警）',
  `controller_report_id` int(11) DEFAULT NULL COMMENT '新版控制器上报记录id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='设备报警信息表';



CREATE TABLE `tab_gb_evt_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `name` varchar(32) NOT NULL COMMENT '国标事件类型名称',
  `type_id` int(11) NOT NULL COMMENT '报警类型id',
  `type_name` varchar(32) NOT NULL COMMENT '报警类型名称',
  `event_state` tinyint(1) NOT NULL DEFAULT '1' COMMENT '事件状态 （0，消失，1，出现，2，丢弃）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='国标事件表';



CREATE TABLE `tab_system_param` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `carousel_time` int(11) NOT NULL DEFAULT '8' COMMENT '轮播时长（单位秒）',
  `crt_sn` varchar(32) COMMENT 'CRT序列号',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='系统参数';



CREATE TABLE `tab_center` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `name` varchar(32) NOT NULL COMMENT '监管中心名称',
  `ip` varchar(32) NOT NULL COMMENT '监管中心ip',
  `port` int(11) NOT NULL COMMENT '监管中线端口号',
  `protocol` varchar(32) NOT NULL DEFAULT 'TCP/IP' COMMENT '通讯协议类型',
  `code` varchar(32) NOT NULL COMMENT '网关编号',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='监管中心';


CREATE TABLE `tab_version` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0 否 1 是）',
  `version_num` varchar(32) DEFAULT NULL COMMENT '版本号',
  `notes` varchar(1024) DEFAULT NULL COMMENT '版本说明',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='系统版本';




INSERT INTO tab_role(is_delete, id, name) VALUES(1, 1, '业主管理人员'),(0, 2, '技术人员'),(0, 3, '业主值班人员');

INSERT INTO tab_user(user_name, password, role_id, role_name) VALUES('superadmin', '086c43497be74645b694ac0ae8fd3165', 3, '业主值班人员');
-- INSERT INTO tab_user(user_name, password, role_id, role_name) VALUES('zhangsan', '72b758fb71d4c585070c7cc102097662', 2, '技术人员');
-- INSERT INTO tab_user(user_name, password, role_id, role_name) VALUES('lisi', '72b758fb71d4c585070c7cc102097662', 2, '技术人员');
-- INSERT INTO tab_user(user_name, password, role_id, role_name) VALUES('test', '72b758fb71d4c585070c7cc102097662', 2, '技术人员');
-- INSERT INTO tab_user(user_name, password, role_id, role_name) VALUES('hukang1', '72b758fb71d4c585070c7cc102097662', 1, '业主管理人员');
-- INSERT INTO tab_user(user_name, password, role_id, role_name) VALUES('sunkang1', '72b758fb71d4c585070c7cc102097662', 1, '业主管理人员');
-- 


INSERT INTO `tab_alarm_type` (`id`, `name`) VALUES (1, '火警');
INSERT INTO `tab_alarm_type` (`id`, `name`) VALUES (2, '启动');
INSERT INTO `tab_alarm_type` (`id`, `name`) VALUES (3, '反馈');
INSERT INTO `tab_alarm_type` (`id`, `name`) VALUES (4, '故障');
INSERT INTO `tab_alarm_type` (`id`, `name`) VALUES (5, '屏蔽');
INSERT INTO `tab_alarm_type` (`id`, `name`) VALUES (6, '监管');
INSERT INTO `tab_alarm_type` (`id`, `name`) VALUES (7, '声光故障');
INSERT INTO `tab_alarm_type` (`id`, `name`) VALUES (8, '声光屏蔽');


INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (1, '正常', 1, '报警事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (2, '首火警', 1, '报警事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (3, '火警', 1, '报警事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (4, '电气火灾报警', 1, '报警事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (5, '可燃气体低限报警', 1, '报警事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (6, '可燃气体高限报警', 1, '报警事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (7, '可燃气体超量程报警', 1, '报警事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (8, '电气火灾预警', 1, '报警事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (20, '启动', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (21, '自动启动', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (22, '手动启动', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (23, '现场急启', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (24, '气体灭火开始延时', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (25, '气体喷洒', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (26, '反馈', 3, '反馈事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (27, '喷洒反馈', 3, '反馈事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (28, '反馈撤销', 3, '反馈事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (29, '停止', 2, '联动事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (30, '现场急停', 2, '联动事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (40, '应急', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (41, '月检', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (42, '年检', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (43, '标志灯具改变方向', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (44, '电梯迫降', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (45, '卷帘半降', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (46, '卷帘全降', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (47, '呼叫', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (48, '通话', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (49, '消防设备电源失电', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (50, '消防设备电源欠压', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (51, '消防设备电源过压', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (52, '消防设备电源过载', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (53, '消防设备电源缺相', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (54, '消防设备电源错相', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (55, '消防水箱（池）水位低', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (56, '消防电梯停用', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (70, '监管', 6, '监管事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (71, '监管解除', 6, '监管事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (72, '屏蔽', 5, '屏蔽事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (73, '屏蔽解除', 5, '屏蔽事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (80, '故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (81, '通讯故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (82, '主电故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (83, '备电故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (84, '充电故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (85, '回路故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (86, '部件故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (87, '线路故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (88, '接地故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (89, '常闭防火门打开', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (90, '常开防火门关闭', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (100, '故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (101, '通讯故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (102, '主电故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (103, '备电故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (104, '充电故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (105, '回路故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (106, '部件故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (107, '线路故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (108, '接地故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (109, '常闭防火门恢复关闭状态', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (110, '常开防火门恢复开门状态', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (120, '开机', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (121, '关机', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (122, '复位', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (123, '自检', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (124, '自检失败', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (127, '手动状态', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (128, '自动状态', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (129, '确认/消音', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (130, '联动控制启动按钮动作', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (131, '检查功能钥匙动作', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (132, '调整时钟', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (210, '查岗应答', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (256, '启动线开路', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (257, '启动线短路', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (258, '停止线开路', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (259, '停止线短路', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (260, '应答线开路', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (261, '掉线故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (262, '地址重号故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (263, '污染故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (264, '备电欠压故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (265, '备电开路故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (266, '主备电故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (267, '备电短路故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (268, '灯具内部故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (269, '主电欠压故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (270, '启动线开路恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (271, '启动线短路恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (272, '停止线开路恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (273, '停止线短路恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (274, '应答线开路恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (275, '掉线故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (276, '地址重号故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (277, '污染故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (278, '备电欠压故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (279, '备电开路故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (280, '主备电故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (281, '备电短路故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (282, '灯具内部故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (283, '主电欠压故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (284, '手工操作允许', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (285, '手工操作禁止', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (290, '注册', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (291, '注册失败', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (292, '解除注册', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (293, '解除注册失败', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (294, '打印机开', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (295, '打印机关', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (296, '联动启动', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (297, '联动消失', 2, '联动事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (298, '反馈缺失', 3, '反馈事件', 2);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (301, '单向指示灯闪亮', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (302, '双向指示灯双闪', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (303, '双向指示灯左闪', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (304, '双向指示灯右闪', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (305, '照明指示灯点亮', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (306, '强点', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (307, '取消强点', 7, '操作事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (308, '强制应急', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (309, '取消强制应急', 7, '操作事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (310, '恢复出厂设置', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (311, '数据备份', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (312, '固件升级', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (313, '传感器故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (314, '传感器故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (315, '消防设备电源欠流', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (316, '消防设备电源欠流恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (317, '消防设备电源失电恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (318, '消防设备电源欠压恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (319, '消防设备电源过压恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (320, '消防设备电源过载恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (321, '消防设备电源缺相恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (322, '消防设备电源错相恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (323, '支路故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (324, '支路故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (326, '左亮', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (327, '右亮', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (328, '全亮', 2, '联动事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (329, '全灭', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (330, '轮响', 2, '联动事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (331, '缺相故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (332, '电压上限报警', 1, '报警事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (333, '电压下限报警', 1, '报警事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (334, '电流上限报警', 1, '报警事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (335, '电流下限报警', 1, '报警事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (336, '漏电流上限报警', 1, '报警事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (337, '温度上限报警', 1, '报警事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (338, '缺相故障恢复', 1, '报警事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (370, '光路故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (371, '光路故障消失', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (372, '感温器件故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (373, '感温器件故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (374, '短路故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (375, '短路故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (376, '输入端开路故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (377, '输入端开路故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (378, '输出端短路故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (379, '输出端短路故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (380, '输出端开路故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (381, '输出端开路故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (382, '内部故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (383, '内部故障消失', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (384, '试用期到期故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (385, '停止端短路故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (386, '停止端短路故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (387, '停止端开路故障', 4, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (388, '停止端开路故障恢复', 4, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (389, '自动模式允许', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (390, '自动模式禁止', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (391, '手动模式允许', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (392, '手动模式禁止', 7, '操作事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (393, '门状态异常', 5, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (394, '门状态异常恢复', 5, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (395, '门反馈缺失', 5, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (396, '闭门到位', 5, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (397, '门接口配置错误', 5, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (398, '门接口配置错误恢复', 5, '故障事件', 0);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (399, '闭门失败', 5, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (400, '供电中断', 5, '故障事件', 1);
INSERT INTO `tab_gb_evt_type` (`id`, `name`, `type_id`, `type_name`, `event_state`) VALUES (401, '供电中断恢复', 7, '操作事件', 0);


INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (1, '报警总线节点', '报警总线节点', 1, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (2, '感烟火灾探测器', '感烟火灾探测器', 2, 1);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (3, '点型感温火灾探测器', '点型感温火灾探测器', 3, 1);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (4, '烟温复合探测器', '烟温复合探测器', 4, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (5, '手动报警按钮', '手动报警按钮', 5, 1);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (6, '消火栓按钮', '消火栓按钮', 6, 1);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (7, '输入模块', '输入模块', 7, 2);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (8, '输入/输出模块', '输入/输出模块', 8, 2);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (9, '4线输出模块', '4线输出模块', 9, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (10, '火灾声光警报器', '火灾声光警报器', 10, 1);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (11, '火灾显示盘', '火灾显示盘', 11, 2);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (12, '短路隔离器', '短路隔离器', 12, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (13, '中继模块', '中继模块', 13, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (14, '火灾报警控制器/火灾报警控制器(联动型)', '火灾报警控制器/火灾报警控制器(联动型)', 14, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (15, '主电源', '主电源', 15, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (16, '备用电源', '备用电源', 16, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (17, '专线盘', '专线盘', 17, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (18, '专线现场模块', '专线现场模块', 18, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (19, '总线盘', '总线盘', 19, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (20, '探测回路', '探测回路', 20, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (21, '回路母板', '回路母板', 21, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (22, '防火门监控器', '防火门监控器', 22, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (25, '消防设备电源监控器', '消防设备电源监控器', 25, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (26, '单相电源电压电流探测器', '单相电源电压电流探测器', 26, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (27, '三相电源电压电流探测器', '三相电源电压电流探测器', 27, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (28, '双路三相电源电压探测器', '双路三相电源电压探测器', 28, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (29, '电气火灾监控设备', '电气火灾监控设备', 29, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (30, '测温式探测器', '测温式探测器', 30, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (31, '剩余电流式电气火灾监控探测器', '剩余电流探测器', 31, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (32, '可燃气体报警控制器', '可燃气体报警控制器', 32, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (33, '可燃气体探测器', 'CO探测器', 33, 4);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (34, '天然气可燃气体探测器', '天然气可燃气体探测器', 34, 4);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (35, '消防电源箱', '消防电源箱', 35, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (36, '气体灭火控制器', '气体灭火控制器', 36, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (40, '气体释放警报器', '气体释放警报器', 40, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (48, '广播模块1403', '广播模块1403', 48, 2);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (78, '单门门磁开关', '防火门门磁开关', 78, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (79, '双门门磁开关', '防火门门磁开关', 79, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (80, '单门门磁开关', '防火门门磁开关', 80, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (81, '双门门磁开关', '防火门门磁开关', 81, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (82, '单门门磁开关', '防火门门磁开关', 82, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (83, '双门门磁开关', '防火门门磁开关', 83, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (84, '防火门电动闭门器', '防火门电动闭门器', 84, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (85, '防火门电动闭门器', '防火门电动闭门器', 85, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (86, '防火门电动闭门器', '防火门电动闭门器', 86, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (87, '组合式电气火灾监控探测器', '8路温度剩余电流探测器', 87, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (88, '紧急启停按钮', '紧急启停按钮', 88, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (89, '输入/输出模块', '输入/输出模块', 89, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (125, '双路三相电源电压电流探测器-P1112/P1116', '双路三相电源电压电流探测器', 125, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (126, '家用有线控制器', '家用有线控制器', 126, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (127, '火灾声光警报器', '火灾声光警报器', 127, 2);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (128, '家用点型观点感烟探测器', '家用点型观点感烟探测器', 128, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (129, '家用点型感温探测器', '家用点型感温探测器', 129, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (201, '家用手动报警开关', '家用手动报警开关', 201, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (209, '三相双路电压单路电流探测器', '三相双路电压单路电流探测器', 209, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (223, '气灭盘', '气灭盘', 223, 5);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (300, 'NB-IoT感烟火灾探测器', 'NB-IoT感烟火灾探测器', 300, 3);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (301, 'NB-IoT感温火灾探测器', 'NB-IoT感温火灾探测器', 301, 4);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (302, 'NB-IoT天然气探测器', 'NB-IoT天然气探测器', 302, 4);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (303, 'NB-IoT液化气探测器', 'NB-IoT液化气探测器', 303, 4);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (304, '家用无线控制器', '家用无线控制器', 304, 4);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (305, 'Lora无线感烟探测器', 'Lora无线感烟探测器', 305, 4);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (306, 'Lora无线感温探测器', 'Lora无线感温探测器', 306, 4);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (307, 'Lora无线手动报警按钮', 'Lora无线手动报警按钮', 307, 4);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (308, 'Lora无线声光警报器', 'Lora无线声光警报器', 308, 4);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (309, 'Lora天然气探测器', 'Lora天然气探测器', 309, 4);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (310, 'Lora液化气探测器', 'Lora液化气探测器', 310, 4);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (311, 'Lora无线输入输出模块', 'Lora无线输入输出模块', 311, 4);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (312, 'NB-IoT无线压力探测器', 'NB-IoT无线压力探测器', 312, 4);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (313, 'NB-IoT无线液位探测器', 'NB-IoT无线液位探测器', 313, 4);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (314, 'NB-IoT无线水浸探测器', 'NB-IoT无线水浸探测器', 314, 4);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (315, 'NB-IoT组合式电气火灾监控探测器', 'NB-IoT组合式电气火灾监控探测器', 315, 4);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (316, 'NB-IoT无线输入输出模块', 'NB-IoT无线输入输出模块', 316, 4);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (317, 'NB-IoT故障电弧探测器', 'NB-IoT故障电弧探测器', 317, 4);
INSERT INTO `tab_device_type` (`id`, `gb_device_type`, `name`, `zx_device_type`, `priority`) VALUES (318, 'NB-IoT智慧用电探测器', 'NB-IoT智慧用电探测器', 318, 4);



-- type 1 项目图片 2 楼宇图片 3 楼层图片 4 应急预案 5 控制室信息 6 系统图
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (1, '系统图_楼宇', 2);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (2, '建筑平面图_楼层', 3);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (3, '消防水源分布图_楼宇_楼层', 6);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (4, '疏散指示图_楼宇_楼层', 6);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (5, '建筑总平面图', 1);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (6, '应急预案', 4);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (7, '系统总图', 6);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (8, '小区规划图', 6);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (9, '电梯图', 6);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (10, '防火门及卷帘系统图', 6);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (11, '消防应急广播图', 6);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (12, '消防电源图', 6);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (13, '自动喷水灭火系统图', 6);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (14, '消火栓系统图', 6);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (15, '气体灭火系统、水喷雾灭火系统图', 6);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (16, '泡沫和干粉灭火系统图', 6);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (17, '防烟排烟图', 6);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (18, '火灾自动报警图', 6);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (19, '消防联动控制图', 6);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (20, '消防水源分布图', 6);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (21, '疏散指示图', 6);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (22, '系统竣工图', 5);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (23, '各分系统控制逻辑说明', 5);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (24, '设备使用说明书', 5);
INSERT INTO `tab_picture_type` (`id`, `name`, `type`) VALUES (25, '值班制度', 5);


INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (2, '感烟火灾探测器', '/static/icon_image/SmokeDetector.png', 2, '感烟火灾探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (3, '点型感温火灾探测器', '/static/icon_image/TemperatureDetector.png', 3, '点型感温火灾探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (4, '烟温复合探测器', '/static/icon_image/CompositeDetector.png', 4, '烟温复合探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (5, '手动报警按钮', '/static/icon_image/ManualAlarmButton.png', 5, '手动报警按钮', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (6, '消火栓按钮', '/static/icon_image/FireHydrantButton.png', 6, '消火栓按钮', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (7, '输入模块', '/static/icon_image/InputModule.png', 7, '输入模块', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (8, '输入/输出模块', '/static/icon_image/InputOutputModule.png', 8, '输入/输出模块', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (9, '4线输出模块', '/static/icon_image/OutputModule.png', 9, '4线输出模块', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (10, '火灾声光警报器', '/static/icon_image/SoundLightAlarm.png', 10, '火灾声光警报器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (11, '火灾显示盘', '/static/icon_image/FloorIndcator.png', 11, '火灾显示盘', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (12, '短路隔离器', '/static/icon_image/RelayModule.png', 12, '短路隔离器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (13, '中继模块', '/static/icon_image/RelayModule.png', 13, '中继模块', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (18, '专线现场模块', '/static/icon_image/RelayModule.png', 18, '专线现场模块', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (26, '单相电源电压电流探测器', '/static/icon_image/fire_equip.png', 26, '单相电源电压电流探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (27, '三相电源电压电流探测器', '/static/icon_image/fire_equip.png', 27, '三相电源电压电流探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (28, '双路三相电源电压探测器', '/static/icon_image/fire_equip.png', 28, '双路三相电源电压探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (30, '测温式探测器', '/static/icon_image/test_wendu.png', 30, '测温式探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (31, '剩余电流探测器', '/static/icon_image/test_dianliu.png', 31, '剩余电流探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (33, 'CO探测器', '/static/icon_image/co.png', 33, 'CO探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (34, '天然气可燃气体探测器', '/static/icon_image/co.png', 34, '天然气可燃气体探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (40, '气体释放警报器', '/static/icon_image/gas_release_alarm.png', 40, '气体释放警报器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (48, '广播模块1403', '/static/icon_image/InputOutputModule.png', 48, '广播模块1403', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (78, '防火门门磁开关', '/static/icon_image/single_magnet.png', 78, '防火门门磁开关', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (79, '防火门门磁开关', '/static/icon_image/double_magnet.png', 79, '防火门门磁开关', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (80, '防火门门磁开关', '/static/icon_image/single_magnet.png', 80, '防火门门磁开关', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (81, '防火门门磁开关', '/static/icon_image/double_magnet.png', 81, '防火门门磁开关', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (82, '防火门门磁开关', '/static/icon_image/single_magnet.png', 82, '防火门门磁开关', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (83, '防火门门磁开关', '/static/icon_image/double_magnet.png', 83, '防火门门磁开关', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (84, '防火门电动闭门器', '/static/icon_image/power_close.png', 84, '防火门电动闭门器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (85, '防火门电动闭门器', '/static/icon_image/power_close.png', 85, '防火门电动闭门器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (86, '防火门电动闭门器', '/static/icon_image/power_close.png', 86, '防火门电动闭门器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (87, '8路温度剩余电流探测器', '/static/icon_image/test_zuhe.png', 87, '8路温度剩余电流探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (88, '紧急启停按钮', '/static/icon_image/em_stop_start.png', 88, '紧急启停按钮', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (89, '输入/输出模块', '/static/icon_image/InputOutputModule.png', 89, '输入/输出模块', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (125, '双路三相电源电压电流探测器', '/static/icon_image/fire_equip.png', 125, '双路三相电源电压电流探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (127, '火灾声光警报器', '/static/icon_image/SoundLightAlarm.png', 127, '火灾声光警报器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (128, '家用点型观点感烟探测器', '/static/icon_image/SmokeDetector.png', 128, '家用点型观点感烟探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (129, '家用点型感温探测器', '/static/icon_image/SmokeDetector.png', 129, '家用点型感温探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (300, 'NB-IoT感烟火灾探测器', '/static/icon_image/SmokeDetector.png', 300, 'NB-IoT感烟火灾探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (301, 'NB-IoT感温火灾探测器', '/static/icon_image/SmokeDetector.png', 301, 'NB-IoT感温火灾探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (302, 'NB-IoT天然气探测器', '/static/icon_image/co.png', 302, 'NB-IoT天然气探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (303, 'NB-IoT液化气探测器', '/static/icon_image/co.png', 303, 'NB-IoT液化气探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (305, 'Lora无线感烟探测器', '/static/icon_image/SmokeDetector.png', 305, 'Lora无线感烟探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (306, 'Lora无线感温探测器', '/static/icon_image/SmokeDetector.png', 306, 'Lora无线感温探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (307, 'Lora无线手动报警按钮', '/static/icon_image/ManualAlarmButton.png', 307, 'Lora无线手动报警按钮', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (308, 'Lora无线声光警报器', '/static/icon_image/SoundLightAlarm2.png', 308, 'Lora无线声光警报器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (309, 'Lora天然气探测器', '/static/icon_image/co.png', 309, 'Lora天然气探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (310, 'Lora液化气探测器', '/static/icon_image/co.png', 310, 'Lora液化气探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (311, 'Lora无线输入输出模块', '/static/icon_image/InputOutputModule.png', 311, 'Lora无线输入输出模块', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (312, 'NB-IoT无线压力探测器', '/static/icon_image/water_gage.png', 312, 'NB-IoT无线压力探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (313, 'NB-IoT无线液位探测器', '/static/icon_image/water_level.png', 313, 'NB-IoT无线液位探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (314, 'NB-IoT无线水浸探测器', '/static/icon_image/water_immersion.png', 314, 'NB-IoT无线水浸探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (315, 'NB-IoT组合式电气火灾监控探测器', '/static/icon_image/test_zuhe.png', 315, 'NB-IoT组合式电气火灾监控探测器', NULL, NULL);
INSERT INTO `tab_icon` (`id`, `name`, `path`, `device_type_id`, `device_type_name`, `gb_evt_type_id`, `gb_evt_type_name`) VALUES (316, 'NB-IoT无线输入输出模块', '/static/icon_image/InputOutputModule.png', 316, 'NB-IoT无线输入输出模块', NULL, NULL);


INSERT INTO `tab_version` (`id`, `version_num`, `notes`) VALUES (1, '3.0.0', '1. 项目初始化');
INSERT INTO `tab_version` (`id`, `version_num`, `notes`) VALUES (2, '3.0.7', '1. 手动替换升级');
