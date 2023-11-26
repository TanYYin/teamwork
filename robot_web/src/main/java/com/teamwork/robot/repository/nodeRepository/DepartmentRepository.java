package com.teamwork.robot.repository.nodeRepository;

import com.teamwork.robot.model.node.Department;
import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.stereotype.Repository;

/**
 * Created with IntelliJ IDEA.
 *
 * @Author: jzy
 * @Date: 2023/11/23/22:43
 * @Description:
 */
@Repository
public interface DepartmentRepository extends Neo4jRepository<Department,Long> {
}
