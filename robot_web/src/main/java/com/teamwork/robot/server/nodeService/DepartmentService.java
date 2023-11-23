package com.teamwork.robot.server.nodeService;

import com.teamwork.robot.model.node.Department;

import java.util.ArrayList;

/**
 * Created with IntelliJ IDEA.
 *
 * @Author: jzy
 * @Date: 2023/11/23/22:42
 * @Description:
 */
public interface DepartmentService {

    ArrayList<Department> getAll();

}
