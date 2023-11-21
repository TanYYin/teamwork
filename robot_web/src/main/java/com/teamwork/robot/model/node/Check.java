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
@NodeEntity(label = "检查")
public class Check {
    @Id
    @GeneratedValue
    private Long id;
    private String name;

    public Check(String name) {
        this.name = name;
    }
}
