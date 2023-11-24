package com.teamwork.robot.controller;

import com.teamwork.robot.model.node.PharmaceuticalEnterprises;
import com.teamwork.robot.service.impl.nodeServiceImpl.PharmaceuticalEnterprisesServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author Xinjie
 * @date 2023/11/25 23:43
 */
@RestController
@RequestMapping("/PharmaceuticalEnterprises")
public class PharmaceuticalEnterprisesController {
    @Autowired
    private PharmaceuticalEnterprisesServiceImpl pharmaceuticalEnterprises;
    @RequestMapping("/findAll")
    public Iterable<PharmaceuticalEnterprises> findAll(){
        return pharmaceuticalEnterprises.getAll();
    }
}
