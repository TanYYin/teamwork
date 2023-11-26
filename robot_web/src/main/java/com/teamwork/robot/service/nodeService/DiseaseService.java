package com.teamwork.robot.service.nodeService;


import com.teamwork.robot.model.node.Disease;
import com.teamwork.robot.result.NodesResult;

import java.util.ArrayList;
import java.util.List;

/**
 * @author Xinjie
 * @date 2023/11/25 23:43
 */
public interface DiseaseService {

    ArrayList<Disease> getAll();


    Disease findByName(String name);

   List<NodesResult> findLow(String diseaseName);


    List<NodesResult> findDisease(String diseaseName);

  /*   List<NodesResult> findFood(String name);


    List<NodesResult> findDepartment(String name);


    List<NodesResult> findDrugs(String name);

    List<NodesResult> findSymptom(String name);

    List<NodesResult> findCheck(String name);

    List<NodesResult> findNotEatFood(String name);

    List<NodesResult> findRecommendDrugs(String diseaseName);

    List<NodesResult> findRecipes(String diseaseName);*/

    /**
     * 添加、删除
     *
     * @param disease 添加和删除的结点
     */
    void modifyDisease(Disease disease);

    /**
     * 删除
     *
     * @param id 疾病id
     */
    void deleteById(String id);

    List<Disease> findNodesByName(String name);
}


