package com.teamwork.robot.model.relationship;

import com.teamwork.robot.model.node.Disease;
import com.teamwork.robot.model.node.Food;
import lombok.Data;
import org.neo4j.ogm.annotation.*;

/**
 * @author Xinjie
 * @date 2023/11/20 23:43
 */
@Data
@RelationshipEntity
public class DoEatRelationship {

    @Id
    @GeneratedValue
    private Long id;
    @StartNode
    private Disease startNode;
    @EndNode
    private Food endNode;
}
