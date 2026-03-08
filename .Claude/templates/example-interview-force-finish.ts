/**
 * 使用模板生成器创建工作流的示例
 *
 * 这个文件展示如何使用 coze-workflow-builder.ts 来生成正确的工作流 JSON
 */

import {
  createWorkflow,
  createCodeNode,
  createHTTPNode,
  resetNodeIdCounter,
} from './coze-workflow-builder';

// 重置计数器（确保每次生成都是从头开始）
resetNodeIdCounter();

// ==================== 定义工作流 ====================

// 步骤1: 构建请求体的代码节点
const buildRequestBodyNode = createCodeNode({
  title: "代码_构建请求体",
  inputs: [
    {
      name: "session_id",
      type: "string",
      sourceNodeId: "10XXXXXX", // 占位符，会被替换为实际的开始节点 ID
      sourceOutputName: "session_id",
    },
  ],
  code: `async function main({ params }: Args): Promise<Output> {
  return {
    requestBody: JSON.stringify({
      session_id: params.session_id
    })
  };
}`,
  outputs: [
    { name: "requestBody", type: "string" },
  ],
});

// 步骤2: HTTP 请求节点
const httpNode = createHTTPNode({
  title: "HTTP_强制结束会话",
  method: "POST",
  url: "http://111.231.51.9:9000/api/coze/question/force-finish",
  headers: [
    { name: "X-API-Key", value: "wehan_open_api_key_2026" },
  ],
  bodyType: "JSON",
  bodySourceNodeId: buildRequestBodyNode.id,
  bodySourceOutputName: "requestBody",
  // ⚠️ 必须提供 JSON 示例内容（即使使用 ref 引用动态变量）
  // Coze 需要这个来渲染请求体 UI 表单
  jsonSchema: JSON.stringify({ session_id: "示例会话ID" }, null, 2),
});

// 步骤3: 解析响应的代码节点
const parseResponseNode = createCodeNode({
  title: "代码_解析响应",
  inputs: [
    {
      name: "responseBody",
      type: "string",
      sourceNodeId: httpNode.id,
      sourceOutputName: "body",
    },
    {
      name: "statusCode",
      type: "integer",
      sourceNodeId: httpNode.id,
      sourceOutputName: "statusCode",
    },
  ],
  code: `async function main({ params }: Args): Promise<Output> {
  const responseBodyStr = params.responseBody;
  const statusCode = params.statusCode;

  // 检查请求是否成功
  if (statusCode !== 200) {
    return {
      code: statusCode,
      msg: "强制结束会话失败",
      data: {
        is_finish: false,
        questions: [],
        answers: [],
        unfinished_questions: []
      }
    };
  }

  // 解析响应数据
  try {
    const response = JSON.parse(responseBodyStr);
    return {
      code: response.code || 200,
      msg: response.msg || "会话已强制结束",
      data: {
        is_finish: true,
        questions: response.data?.questions || [],
        answers: response.data?.answers || [],
        unfinished_questions: response.data?.unfinished_questions || [],
        total_questions: response.data?.total_questions || 0,
        completed_count: response.data?.completed_count || 0
      }
    };
  } catch (e) {
    return {
      code: 500,
      msg: "解析响应失败",
      data: {
        is_finish: false,
        questions: [],
        answers: [],
        unfinished_questions: []
      }
    };
  }
}`,
  outputs: [
    { name: "code", type: "integer" },
    { name: "msg", type: "string" },
    { name: "data", type: "object" },
  ],
});

// ==================== 生成完整工作流 ====================

const workflow = createWorkflow({
  startOutputs: [
    { name: "session_id", type: "string", required: true },
  ],
  endInputs: [
    {
      name: "code",
      type: "integer",
      sourceNodeId: parseResponseNode.id,
      sourceOutputName: "code",
    },
    {
      name: "msg",
      type: "string",
      sourceNodeId: parseResponseNode.id,
      sourceOutputName: "msg",
    },
    {
      name: "data",
      type: "object",
      sourceNodeId: parseResponseNode.id,
      sourceOutputName: "data",
    },
  ],
  nodes: [buildRequestBodyNode, httpNode, parseResponseNode],
});

// ==================== 修复节点引用 ====================

// 由于开始节点 ID 是动态生成的，需要更新引用
const startNodeId = workflow.json.nodes[0].id;
const codeNode1Id = workflow.json.nodes[1].id;

// 更新第一个代码节点的输入引用
workflow.json.nodes[1].data.inputs.inputParameters[0].input.value.content.blockID = startNodeId;

// 写入文件（不输出到 stdout，避免污染重定向）
import { writeFileSync } from 'fs';
writeFileSync(
  'E:\\文档\\code\\WeHan\\client\\workflows\\interview_force_finish_workflow.json',
  JSON.stringify(workflow, null, 2),
  'utf-8'
);
console.error('✅ 工作流已生成到: interview_force_finish_workflow.json');
