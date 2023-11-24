package com.teamwork.robot.repository.nodeRepository;

import com.teamwork.robot.model.node.Symptom;
import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.stereotype.Repository;

/**
 * @author Crystry
 * @date 2021/11/22 21:59
 */

@Repository
public interface SymptomRepository extends Neo4jRepository<Symptom,Long> {
}
