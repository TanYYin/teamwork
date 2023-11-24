package com.teamwork.robot.service.impl.nodeServiceImpl;


import com.google.common.collect.Lists;
import com.teamwork.robot.model.node.Disease;
import com.teamwork.robot.repository.nodeRepository.DiseaseRepository;
import com.teamwork.robot.repository.relationshipRepo.AcompanyWithRelationshipRepo;
import com.teamwork.robot.repository.relationshipRepo.OtherRelationshipRepo;
import com.teamwork.robot.result.NodesResult;
import com.teamwork.robot.service.nodeService.DiseaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

/**
 * @author Xinjie
 * @date 2023/11/25 23:43
 */
@Service
public class DiseaseServiceImpl implements DiseaseService {

    @Autowired
    private DiseaseRepository diseaseRepository;
    @Autowired
    private OtherRelationshipRepo otherRelationshipRepo;

    @Autowired
    private AcompanyWithRelationshipRepo acompanyWithRelationshipRepo;

    /**
     * 查询全部
     * @return 返回全部疾病信息
     */
    @Override
    public ArrayList<Disease> getAll() {
        Iterable<Disease> all = diseaseRepository.findAll();
        ArrayList<Disease> diseases = Lists.newArrayList(all);
        System.out.println(diseases);
        return diseases;
    }

    /**
     * 根据结点名称查询
     * @param name 疾病名称
     * @return 疾病信息
     */
    @Override
    public Disease findByName(String name) {
        return diseaseRepository.findNodeByName(name);
    }

    @Override
    public List<NodesResult> findLow(String diseaseName) {
        return otherRelationshipRepo.findLow(diseaseName);
    }

    @Override
    public List<NodesResult> findDisease(String diseaseName) {
        return acompanyWithRelationshipRepo.findLowByName(diseaseName);
    }

    /**
     * 根据结点名称查询
     * @param name 疾病名称
     * @return 疾病信息
     */
    @Override
    public List<Disease> findNodesByName(String name) {
        return diseaseRepository.findNodesByName(name);
    }

  /*  *//**
     * 返回疾病do_eat的食物
     * @param name 疾病名称
     * @return 疾病相关食物
     *//*
    @Override
    public List<NodesResult> findFood(String name) {
        return otherRelationshipRepo.findFood(name);
    }

    *//**
     *
     * @param name 疾病名称
     * @return 返回疾病所属的部门 科室
     *//*
    @Override
    public List<NodesResult> findDepartment(String name) {
        return otherRelationshipRepo.findDepartment(name);
    }

    *//**
     *
     * @param name 疾病名称
     * @return 返回疾病所属的药物
     *//*
    @Override
    public List<NodesResult> findDrugs(String name) {
        return otherRelationshipRepo.findDrugs(name);
    }

    *//**
     *
     * @param name 疾病名称
     * @return 返回疾病的症状
     *//*
    @Override
    public List<NodesResult> findSymptom(String name) {
        return otherRelationshipRepo.findSymptom(name);
    }

    *//**
     *
     * @param name 疾病名称
     * @return 返回疾病需要做的检查
     *//*
    @Override
    public List<NodesResult> findCheck(String name) {
        return otherRelationshipRepo.findCheck(name);
    }

    *//**
     *
     * @param name 疾病名称
     * @return 返回疾病不能吃的药品
     *//*
    @Override
    public List<NodesResult> findNotEatFood(String name) {
        return otherRelationshipRepo.findNotEatFood(name);
    }

    *//**
     *
     * @param diseaseName 疾病名称
     * @return  返回疾病recommend_drug
     *//*
    @Override
    public List<NodesResult> findRecommendDrugs(String diseaseName) {
        return otherRelationshipRepo.findRecommendDrugs(diseaseName);
    }

    *//**
     *
     * @param diseaseName 疾病名称
     * @return 返回疾病可使用的菜谱
     *//*
    @Override
    public List<NodesResult> findRecipes(String diseaseName) {
        return otherRelationshipRepo.findRecipes(diseaseName);
    }
*/
    /**
     *
     * @param disease  添加和删除的结点
     */
    @Override
    public void modifyDisease(Disease disease) {
        diseaseRepository.save(disease);
    }

    /**
     * 删除
     *
     * @param id 疾病id
     */
    @Override
    public void deleteById(String id) {
        diseaseRepository.deleteById(Long.valueOf(id));
    }

}
