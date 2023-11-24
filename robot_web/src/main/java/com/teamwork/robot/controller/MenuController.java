package com.teamwork.robot.controller;


import com.teamwork.robot.model.node.Menu;
import com.teamwork.robot.service.impl.nodeServiceImpl.MenuServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author Xinjie
 * @date 2023/11/25 23:43
 */
@RestController
@RequestMapping("/menu")
public class MenuController {
    @Autowired
    private MenuServiceImpl menuService;
    @RequestMapping("/findAll")
    public Iterable<Menu> findAll(){
        return menuService.getAll();
    }
}
