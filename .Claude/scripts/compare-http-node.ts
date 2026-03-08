/**
 * HTTP 节点结构对比检查工具
 * 用于验证生成的 JSON 是否符合配置指南
 */

import { readFileSync } from 'fs';

interface HTTPNode {
  type: string;
  data: {
    inputs: {
      apiInfo?: { method: string; url: string };
      body?: {
        bodyType: string;
        bodyData: any;
      };
      headers?: any[];
      params?: any[];
      auth?: any;
      setting?: any;
      settingOnError?: any;
    };
    outputs?: Array<{ type: string; name: string }>;
    settingOnError?: any;
  };
}

function checkHTTPNode(filePath: string) {
  const content = readFileSync(filePath, 'utf-8');
  const workflow = JSON.parse(content);

  // 找到 HTTP 节点
  const httpNodes = workflow.json.nodes.filter((n: any) => n.type === '45');

  if (httpNodes.length === 0) {
    console.log('❌ 未找到 HTTP 节点');
    return;
  }

  console.log(`✅ 找到 ${httpNodes.length} 个 HTTP 节点\n`);

  httpNodes.forEach((node: HTTPNode, index: number) => {
    console.log(`\n=== HTTP 节点 #${index + 1} (${node.data.nodeMeta?.title || '未命名'}) ===\n`);

    const inputs = node.data.inputs;
    const issues: string[] = [];
    const passes: string[] = [];

    // 检查 1: apiInfo 结构
    if (inputs.apiInfo) {
      const apiInfoKeys = Object.keys(inputs.apiInfo);
      if (apiInfoKeys.length === 2 && apiInfoKeys.includes('method') && apiInfoKeys.includes('url')) {
        passes.push('✅ apiInfo 只包含 method 和 url');
      } else {
        issues.push(`❌ apiInfo 包含额外字段: ${apiInfoKeys.join(', ')}`);
      }

      if (typeof inputs.apiInfo.url === 'string') {
        passes.push('✅ url 是字符串');
      } else {
        issues.push('❌ url 不是字符串');
      }
    } else {
      issues.push('❌ 缺少 apiInfo');
    }

    // 检查 2: inputs 直接子字段
    const requiredFields = ['body', 'headers', 'params', 'auth', 'setting', 'settingOnError'];
    const inputsFields = Object.keys(inputs).filter(k => k !== 'apiInfo');

    if (inputsFields.includes('body') && inputsFields.includes('headers')) {
      passes.push('✅ body 和 headers 是 inputs 的直接子字段');
    } else {
      issues.push(`❌ body 或 headers 不是 inputs 的直接子字段`);
    }

    // 检查 3: headers 不为空
    if (inputs.headers && inputs.headers.length > 0) {
      passes.push(`✅ headers 包含 ${inputs.headers.length} 个请求头`);
    } else {
      issues.push('❌ headers 为空数组');
    }

    // 检查 4: bodyData 结构
    if (inputs.body?.bodyData) {
      const bodyData = inputs.body.bodyData;

      // 检查顶层字段
      const hasContent = bodyData.content !== undefined;
      const hasRawMeta = bodyData.rawMeta !== undefined;
      const hasBinary = bodyData.binary !== undefined;
      const hasJson = bodyData.json !== undefined;

      if (inputs.body.bodyType === 'JSON') {
        if (hasContent && hasRawMeta && hasBinary && hasJson) {
          passes.push('✅ JSON bodyType: bodyData 包含完整的 4 个字段 (content, rawMeta, binary, json)');
        } else {
          issues.push(`❌ JSON bodyType: bodyData 缺少字段 - content:${hasContent}, rawMeta:${hasRawMeta}, binary:${hasBinary}, json:${hasJson}`);
        }

        // 检查 rawMeta 位置（应该在 value 内部）
        const rawMetaInValue = bodyData.binary?.fileURL?.value?.rawMeta !== undefined;
        if (rawMetaInValue) {
          passes.push('✅ rawMeta 在 value 对象内部');
        } else {
          issues.push('❌ rawMeta 不在 value 对象内部');
        }
      } else if (inputs.body.bodyType === 'EMPTY') {
        if (hasContent && hasRawMeta && hasBinary && hasJson) {
          passes.push('✅ EMPTY bodyType: bodyData 包含完整的 4 个字段');
        } else {
          issues.push(`❌ EMPTY bodyType: bodyData 缺少字段`);
        }
      }
    }

    // 检查 5: outputs 类型
    if (node.data.outputs) {
      const bodyOutput = node.data.outputs.find((o: any) => o.name === 'body');
      if (bodyOutput && bodyOutput.type === 'string') {
        passes.push('✅ outputs.body 类型是 string');
      } else {
        issues.push('❌ outputs.body 类型不是 string');
      }
    }

    // 检查 6: data.settingOnError
    if (node.data.settingOnError !== undefined) {
      passes.push('✅ data.settingOnError 存在');
    } else {
      issues.push('❌ 缺少 data.settingOnError');
    }

    // 打印结果
    console.log('📋 检查结果:');
    console.log('');
    passes.forEach(p => console.log('  ' + p));
    issues.forEach(i => console.log('  ' + i));

    if (issues.length === 0) {
      console.log('\n🎉 所有检查通过！');
    } else {
      console.log(`\n⚠️ 发现 ${issues.length} 个问题`);
    }
  });
}

// 运行检查
const filePath = process.argv[2] || 'E:\\文档\\code\\WeHan\\client\\workflows\\interview_force_finish_workflow.json';
console.log(`\n🔍 检查文件: ${filePath}\n`);
checkHTTPNode(filePath);
