package com.hei.robot.service.nodeService;


import com.hei.robot.model.node.Disease;
import com.hei.robot.result.NodesResult;
import org.springframework.data.neo4j.annotation.Query;

import java.util.ArrayList;
import java.util.List;

/**
 * @author Crystry
 * @date 2021/11/22 20:27
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


