package com.teamwork.robot.service.impl.nodeServiceImpl;

import com.teamwork.robot.repository.relationshipRepo.OtherRelationshipRepo;
import com.teamwork.robot.result.DiseaseResult;
import com.teamwork.robot.service.nodeService.PublicService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @author Xinjie
 * @date 2023/11/25 23:43
 */
@Service
public class PublicServiceImpl implements PublicService {
    @Autowired
    private OtherRelationshipRepo otherRelationshipRepo;

    @Override
    public List<DiseaseResult> findDisease(String name) {
        return otherRelationshipRepo.findDisease(name);
    }
}
