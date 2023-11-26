package com.teamwork.robot.repository.relationshipRepo;

import com.teamwork.robot.model.relationship.AccompanyWithRelationship;
import com.teamwork.robot.result.NodesResult;
import org.springframework.data.neo4j.annotation.Query;
import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * @author Crystry
 * @date 2021/11/22 23:31
 */
@Repository
public interface AcompanyWithRelationshipRepo extends Neo4jRepository<AccompanyWithRelationship,Long> {

    @Query("match (a:`疾病`)-[r:acompany_with]->(b) where a.name={name} return b.name as name")
    List<NodesResult> findLowByName(String name);

}
