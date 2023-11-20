package com.teamwork.robot.model.node;

import lombok.Data;
import org.neo4j.ogm.annotation.GeneratedValue;
import org.neo4j.ogm.annotation.Id;
import org.neo4j.ogm.annotation.NodeEntity;

/**
 * @author Xinjie
 * @date 2023/11/20 23:43
 */
@Data
@NodeEntity(label = "疾病")
public class Disease {
    @Id
    @GeneratedValue
    private Long id;
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

    public Disease(String name, String prevent, String get_prob, String symptom, String[] cure_way, String cure_lasttime, String cured_prob, String cause, String[] cure_department, String easy_get, String desc) {
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
    }
}
