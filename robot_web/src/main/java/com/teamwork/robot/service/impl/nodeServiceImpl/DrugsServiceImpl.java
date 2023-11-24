package com.teamwork.robot.service.impl.nodeServiceImpl;


import com.google.common.collect.Lists;
import com.teamwork.robot.model.node.Drugs;
import com.teamwork.robot.repository.nodeRepository.DrugsRepository;
import com.teamwork.robot.service.nodeService.DrugsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;

/**
 * @author Xinjie
 * @date 2023/11/25 23:43
 */
@Service
public class DrugsServiceImpl implements DrugsService {

    @Autowired
    private DrugsRepository drugsRepository;

    @Override
    public ArrayList<Drugs> getAll() {
        Iterable<Drugs> all = drugsRepository.findAll();
        ArrayList<Drugs> checks = Lists.newArrayList(all);
        System.out.println(checks);
        return checks;
    }
}


