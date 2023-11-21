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
@NodeEntity(label = "药企")
public class PharmaceuticalEnterprises {
    @Id
    @GeneratedValue
    private Long id;
    private String name;

    public PharmaceuticalEnterprises(String name) {
        this.name = name;
    }
}
