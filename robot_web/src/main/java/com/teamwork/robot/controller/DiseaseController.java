package com.teamwork.robot.controller;

import com.teamwork.robot.model.node.Disease;
import com.teamwork.robot.repository.relationshipRepo.OtherRelationshipRepo;
import com.teamwork.robot.result.NodesResult;
import com.teamwork.robot.result.Result;
import com.teamwork.robot.service.impl.nodeServiceImpl.DiseaseServiceImpl;
import com.teamwork.robot.util.IsEmptyUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

/**
 * @author Xinjie
 * @date 2023/11/25 23:43
 */
@RestController
@RequestMapping("/disease")
public class DiseaseController {
    @Autowired
    private DiseaseServiceImpl diseaseService;
    //计数
    private int COUNT = 0;
    //查询所有疾病所有内容
    private ArrayList<Disease> all = new ArrayList<>();

    /**
     *
     * @return 返回所有疾病信息
     */
    @RequestMapping("/findAll")
    public ArrayList<Disease> findAll() {
        return diseaseService.getAll();
    }

    /**
     * @param name 疾病名称
     * @return 根据名称查询疾病节点信息
     */
    @RequestMapping("/findMessageFromDisease/{name}")
    public Result<Disease> findMessageByName(@PathVariable("name") String name) {
        return IsEmptyUtil.IsEmptyAndSizeItem(diseaseService.findByName(name));
    }

    /**
     * @param name 疾病名称
     * @return 根据名称查询疾病节点信息
     */
    @Autowired
    private OtherRelationshipRepo otherRelationshipRepo;
    @RequestMapping("/findAllMessageFromDisease/{name}")
    public Result<List<NodesResult>> a(@PathVariable("name") String name) {
        return IsEmptyUtil.IsEmptyAndSize(otherRelationshipRepo.findLow(name));
    }

    /**
     * @param disease 疾病信息
     * @return 返回修改或者添加后的信息
     */
    @RequestMapping(value = "/modifyDisease", method = RequestMethod.POST)
    public Result<Disease> modify(@ModelAttribute("Disease") Disease disease) {
            if (all.size() == 0) {
                all = diseaseService.getAll();
            }
            boolean flag=false;
            for (int i = 0; i < all.size(); i++) {
                if (all.get(i).getName().equals(disease.getName())){
                    flag=true;
                    COUNT=i;
                    break;
                }
            }
        if (flag){
            disease.setId(all.get(COUNT).getId());
            //修改数据
            diseaseService.modifyDisease(disease);
            disease = diseaseService.findByName(disease.getName());
            all.set(COUNT,disease);
        }else {
            //如果不存在，则添加
            diseaseService.modifyDisease(disease);
            disease = diseaseService.findByName(disease.getName());
            System.out.println(disease);
            all.add(disease);
        }
        return IsEmptyUtil.IsEmptyAndSizeItem(disease);
    }

    /**
     * 删除
     *
     * @param id 需要删除的节点id
     */
    @RequestMapping(value = "/delete/{id}")
    public void deleteById(@PathVariable(value = "id") String id) {
        diseaseService.deleteById(id);
        }

}