package com.teamwork.robot.result;

import lombok.Data;
import org.springframework.data.neo4j.annotation.QueryResult;

/**
 * 结点属性
 *
 * @author Xinjie
 * @date 2023/11/20 23:43
 */
@Data
@QueryResult //接受neo4j返回的数据
public class NodesResult {

    private String type;

    /**
     * 结点属性 name
     */
    private String name;
}
