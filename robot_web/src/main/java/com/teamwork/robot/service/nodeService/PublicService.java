package com.teamwork.robot.service.nodeService;

import com.teamwork.robot.result.DiseaseResult;

import java.util.List;

/**
 * @author Xinjie
 * @date 2023/11/25 23:43
 */
public interface PublicService {

    List<DiseaseResult> findDisease(String checkName);

}
