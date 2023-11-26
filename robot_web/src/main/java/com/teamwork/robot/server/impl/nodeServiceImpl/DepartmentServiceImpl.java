package com.teamwork.robot.server.impl.nodeServiceImpl;

import com.google.common.collect.Lists;
import com.teamwork.robot.model.node.Department;
import com.teamwork.robot.repository.nodeRepository.DepartmentRepository;
import com.teamwork.robot.server.nodeService.DepartmentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;

/**
 * Created with IntelliJ IDEA.
 *
 * @Author: jzy
 * @Date: 2023/11/23/22:41
 * @Description:
 */
@Service
public class DepartmentServiceImpl implements DepartmentService {

    @Autowired
    private DepartmentRepository departmentRepository;

    @Override
    public ArrayList<Department> getAll() {
        Iterable<Department> all = departmentRepository.findAll();
        ArrayList<Department> departments = Lists.newArrayList(all);
        return departments;
    }


}
