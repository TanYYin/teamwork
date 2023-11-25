package com.teamwork.robot.repository.nodeRepository;

import com.teamwork.robot.model.node.Drugs;
import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.stereotype.Repository;

/**
 * Created with IntelliJ IDEA.
 *
 * @Author: jzy
 * @Date: 2023/11/25/22:06
 * @Description:
 */
@Repository
public interface DrugsRepository extends Neo4jRepository<Drugs,Long> {
}
