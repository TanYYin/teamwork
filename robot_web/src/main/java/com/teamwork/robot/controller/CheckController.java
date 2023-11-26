package com.teamwork.robot.controller;

import com.teamwork.robot.model.node.Check;
import com.teamwork.robot.service.impl.nodeServiceImpl.CheckServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author Xinjie
 * @date 2023/11/25 23:43
 */
@RestController
@RequestMapping("/check")
public class CheckController {

    @Autowired
    private CheckServiceImpl checkService;

    @RequestMapping("/findAll")
    public Iterable<Check> findAll(){
        return checkService.getAll();
    }
}
