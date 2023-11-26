package com.teamwork.robot.service.impl.nodeServiceImpl;


import com.google.common.collect.Lists;
import com.teamwork.robot.model.node.Food;
import com.teamwork.robot.repository.nodeRepository.FoodRepository;
import com.teamwork.robot.service.nodeService.FoodService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;

/**
 * @author Xinjie
 * @date 2023/11/25 23:43
 */
@Service
public class FoodServiceImpl implements FoodService {

    @Autowired
    private FoodRepository foodRepository;

    @Override
    public ArrayList<Food> getAll() {
        Iterable<Food> all = foodRepository.findAll();
        ArrayList<Food> foods = Lists.newArrayList(all);
        System.out.println(foods);
        return foods;
    }


}
