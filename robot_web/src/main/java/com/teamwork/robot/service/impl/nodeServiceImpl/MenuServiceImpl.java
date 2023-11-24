package com.teamwork.robot.service.impl.nodeServiceImpl;


import com.google.common.collect.Lists;
import com.teamwork.robot.model.node.Menu;
import com.teamwork.robot.repository.nodeRepository.MenuRepository;
import com.teamwork.robot.service.nodeService.MenuService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;

/**
 * @author Xinjie
 * @date 2023/11/25 23:43
 */
@Service
public class MenuServiceImpl implements MenuService {

    @Autowired
    private MenuRepository menuRepository;

    @Override
    public ArrayList<Menu> getAll() {
        Iterable<Menu> all = menuRepository.findAll();
        ArrayList<Menu> checks = Lists.newArrayList(all);
        System.out.println(checks);
        return checks;
    }

}
