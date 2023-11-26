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
@NodeEntity(label = "症状")
public class Symptom {
    @Id
    @GeneratedValue
    private Long id;
    private String name;

    public Symptom(String name) {
        this.name = name;
    }
}
