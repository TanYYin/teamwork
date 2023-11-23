package com.teamwork.robot.server.impl.nodeServiceImpl;

import com.google.common.collect.Lists;
import com.teamwork.robot.model.node.Check;
import com.teamwork.robot.repository.nodeRepository.CheckRepository;
import com.teamwork.robot.server.nodeService.CheckService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;

/**
 * Created with IntelliJ IDEA.
 *
 * @Author: jzy
 * @Date: 2023/11/22/15:31
 * @Description:
 */
@Service
public class CheckServiceImpl implements CheckService {

    @Autowired
    private CheckRepository checkRepository;

    @Override
    public ArrayList<Check> getAll() {
        Iterable<Check> all = checkRepository.findAll();
        ArrayList<Check> checks = Lists.newArrayList(all);
        return checks;
    }

}
