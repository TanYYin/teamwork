package com.teamwork.robot.controller;

import com.teamwork.robot.model.node.Drugs;
import com.teamwork.robot.server.impl.nodeServiceImpl.DrugsServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Created with IntelliJ IDEA.
 *
 * @Author: jzy
 * @Date: 2023/11/25/22:04
 * @Description:
 */
@RestController
@RequestMapping("/drugs")
public class DrugsController {
    @Autowired
    private DrugsServiceImpl drugsService;
    @RequestMapping("/findAll")
    public Iterable<Drugs> findAll(){
        return drugsService.getAll();
    }
}