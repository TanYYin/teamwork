package com.teamwork.robot.controller;

import com.teamwork.robot.model.node.Department;
import com.teamwork.robot.server.impl.nodeServiceImpl.DepartmentServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Created with IntelliJ IDEA.
 *
 * @Author: jzy
 * @Date: 2023/11/23/22:41
 * @Description:
 */
@RestController
@RequestMapping("/department")
public class DepartmentController {
    @Autowired
    private DepartmentServiceImpl departmentService;
    @RequestMapping("/findAll")
    public Iterable<Department> findAll(){
        return departmentService.getAll();
    }
}
