package com.teamwork.robot.controller;

import com.teamwork.robot.model.node.Check;
import com.teamwork.robot.server.impl.nodeServiceImpl.CheckServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Created with IntelliJ IDEA.
 *
 * @Author: jzy
 * @Date: 2023/11/22/11:48
 * @Description:
 */
@RestController
@RequestMapping("/symptom")
public class SymptomController {
    @Autowired
    private CheckServiceImpl checkService;
    @RequestMapping("/findAll")
    public Iterable<Check> findAll(){
        return checkService.getAll();
    }
}
