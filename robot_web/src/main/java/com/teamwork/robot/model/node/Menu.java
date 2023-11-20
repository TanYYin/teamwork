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
@NodeEntity(label = "菜谱")
public class Menu {
    @Id
    @GeneratedValue
    private Long id;
    private String name;

    public Menu(String name) {
        this.name = name;
    }
}
