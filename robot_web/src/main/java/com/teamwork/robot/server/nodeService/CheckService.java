package com.teamwork.robot.server.nodeService;

import com.teamwork.robot.model.node.Check;

import java.util.ArrayList;

/**
 * Created with IntelliJ IDEA.
 *
 * @Author: jzy
 * @Date: 2023/11/22/15:30
 * @Description:
 */
public interface CheckService {
    /**
     * 查询全部
     * @return 返回全部信息
     */
    ArrayList<Check> getAll();


}
