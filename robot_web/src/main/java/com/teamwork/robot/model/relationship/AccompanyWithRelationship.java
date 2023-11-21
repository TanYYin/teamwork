package com.teamwork.robot.model.relationship;

import com.teamwork.robot.model.node.Disease;
import lombok.Data;
import org.neo4j.ogm.annotation.*;

/**
 * @author Xinjie
 * @date 2023/11/20 23:43
 */
@Data
@RelationshipEntity(type = "acompany_with")
public class AccompanyWithRelationship {
    @Id
    @GeneratedValue
    private Long id;
    @StartNode
    private Disease startNode;
    @EndNode
    private Disease endNode;

}
