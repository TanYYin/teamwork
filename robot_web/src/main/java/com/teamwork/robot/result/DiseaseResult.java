package com.teamwork.robot.result;

import com.teamwork.robot.model.node.Disease;
import lombok.Data;
import org.springframework.data.neo4j.annotation.QueryResult;

/**
 * @author Xinjie
 * @date 2023/11/20 23:43
 */
@Data
@QueryResult //接受neo4j返回的数据
public class DiseaseResult{
    private String type;
    private Disease disease;
/*
    private String name;
    private String prevent;
    private String get_prob;
    private String symptom;
    private String[] cure_way;
    private String cure_lasttime;
    private String cured_prob;
    private String cause;
    private String[] cure_department;
    private String easy_get;
    private String desc;
*/

    public DiseaseResult(String type, Disease disease) {
        this.type = type;
        this.disease = disease;
    }

    /*    public DiseaseResult(String type, String name, String prevent, String get_prob, String symptom, String[] cure_way, String cure_lasttime, String cured_prob, String cause, String[] cure_department, String easy_get, String desc) {
        this.type = type;
        this.name = name;
        this.prevent = prevent;
        this.get_prob = get_prob;
        this.symptom = symptom;
        this.cure_way = cure_way;
        this.cure_lasttime = cure_lasttime;
        this.cured_prob = cured_prob;
        this.cause = cause;
        this.cure_department = cure_department;
        this.easy_get = easy_get;
        this.desc = desc;
    }*/
}
