package com.teamwork.robot.controller;

import com.teamwork.robot.result.DiseaseResult;
import com.teamwork.robot.result.Result;
import com.teamwork.robot.service.impl.nodeServiceImpl.PublicServiceImpl;
import com.teamwork.robot.util.CacheOperator;
import com.teamwork.robot.util.IsEmptyUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;


/**
 * @author Xinjie
 * @date 2023/11/25 23:43
 */
@RestController
@RequestMapping("/public")
public class publicController {

    @Autowired
    private PublicServiceImpl publicService;

    /**
     *
     * @param name 查询的名字
     * @return 返回与之相关的疾病信息
     */
    @RequestMapping("/findDisease/{name}")
    public Result<List<DiseaseResult>> findDisease(@PathVariable(value = "name") String name) {
        return IsEmptyUtil.IsEmptyAndSize(publicService.findDisease(name));
    }

    @RequestMapping("/getCache")
    public String getCache(){
        return CacheOperator.showCache();
    }

    @RequestMapping(value = "/addCache/{key}/{value}")
    public boolean addCache(@PathVariable(value = "key")String key,@PathVariable(value = "value")String value){

      return CacheOperator.addCache(key,value);

    }

    @RequestMapping("/updateCache/{key}/{value}")
    public boolean updateCache(@PathVariable(value = "key")String key,@PathVariable(value = "value")String value){
       return CacheOperator.updateCache(key, value);
    }

    @RequestMapping("/deleteCache/{key}")
    public boolean deleteCache(@PathVariable(value = "key")String key){
       return CacheOperator.deleteCache(key);
    }



}
