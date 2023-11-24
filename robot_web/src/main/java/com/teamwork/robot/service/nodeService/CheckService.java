package com.teamwork.robot.service.nodeService;

import com.teamwork.robot.model.node.Check;

import java.util.ArrayList;

/**
 * @author Xinjie
 * @date 2023/11/25 23:43
 */
public interface CheckService {
    /**
     * 查询全部
     * @return 返回全部信息
     */
    ArrayList<Check> getAll();

}
