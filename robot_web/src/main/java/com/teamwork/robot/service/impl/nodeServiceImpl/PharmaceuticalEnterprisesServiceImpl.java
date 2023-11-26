package com.teamwork.robot.service.impl.nodeServiceImpl;


import com.google.common.collect.Lists;
import com.teamwork.robot.model.node.PharmaceuticalEnterprises;
import com.teamwork.robot.repository.nodeRepository.PharmaceuticalEnterprisesRepository;
import com.teamwork.robot.service.nodeService.PharmaceuticalEnterprisesService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;

/**
 * @author Xinjie
 * @date 2023/11/25 23:43
 */
@Service
public class PharmaceuticalEnterprisesServiceImpl implements PharmaceuticalEnterprisesService {

    @Autowired
    private PharmaceuticalEnterprisesRepository pharmaceuticalEnterprises;

    @Override
    public ArrayList<PharmaceuticalEnterprises> getAll() {
        Iterable<PharmaceuticalEnterprises> all = pharmaceuticalEnterprises.findAll();
        ArrayList<PharmaceuticalEnterprises> pharmaceuticalEnterprises = Lists.newArrayList(all);
        System.out.println(pharmaceuticalEnterprises);
        return pharmaceuticalEnterprises;
    }

}
