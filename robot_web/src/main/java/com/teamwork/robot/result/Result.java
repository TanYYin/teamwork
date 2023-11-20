package com.teamwork.robot.result;

import lombok.Data;

/**
 * @author Xinjie
 * @date 2023/11/20 23:46
 * <p>
 * {status=0, code=500, msg='查询成功', data=数据}
 * {status=0, code=204, msg='查询成功无记录', data=[]}
 * {status=1, code=500, msg='参数为空或格式错误', data=[]}
 */

@Data
public class Result<T> {
    /**
     * 处理结果: 0 : 成功  1 : 失败 。和错误编码区分
     * 参数格式错误 赋值为1 发生异常，查询出错 赋值为1  查询成功 没有错误 都设定为0
     */
    private Integer status;

    /**
     * 服务器返回的业务编码
     */
    private Integer code;

    /**
     * 服务器返回的提示信息（包括成功提示消息和错误消息）
     */
    private String msg;

    /**
     * 服务器的返回数据（即使出错，也要返回空对象，不能直接返回null）
     */
    private T data;

    /**
     * 返回数据的记录条数
     */
    private Long size;

    /**
     * 构造器
     */
    public Result(Integer status, Integer code, String msg) {
        this.status = status;
        this.code = code;
        this.msg = msg;
    }

    public Result(Integer status, Integer code, String msg, T data, Long size) {
        this.status = status;
        this.code = code;
        this.msg = msg;
        this.data = data;
        this.size = size;
    }
}
