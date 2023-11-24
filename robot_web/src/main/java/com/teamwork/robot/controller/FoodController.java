package com.teamwork.robot.controller;

import com.teamwork.robot.model.node.Food;
import com.teamwork.robot.service.impl.nodeServiceImpl.FoodServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author Xinjie
 * @date 2023/11/25 23:43
 */
@RestController
@RequestMapping("/food")
public class FoodController {
    @Autowired
    private FoodServiceImpl foodService;
    @RequestMapping("/findAll")
    public Iterable<Food> findAll(){
        return foodService.getAll();
    }
}
