package com.teamwork.robot.controller;

import com.teamwork.robot.model.node.Drugs;
import com.teamwork.robot.service.impl.nodeServiceImpl.DrugsServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author Xinjie
 * @date 2023/11/25 23:43
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
