import request from 'supertest';
import { createServer } from '../src/server.js';

jest.mock('../src/github/client.js', () => ({
  GitHubClient: jest.fn().mockImplementation(() => ({
    delegateToCopilot: jest.fn(),
  })),
}));

jest.mock('../src/integrations/jira/handler.js', () => ({
  JiraHandler: jest.fn().mockImplementation(() => ({
    handle: jest.fn().mockResolvedValue(undefined),
  })),
}));

jest.mock('../src/integrations/azure-boards/handler.js', () => ({
  AzureBoardsHandler: jest.fn().mockImplementation(() => ({
    handle: jest.fn().mockResolvedValue(undefined),
  })),
}));

jest.mock('../src/integrations/linear/handler.js', () => ({
  LinearHandler: jest.fn().mockImplementation(() => ({
    handle: jest.fn().mockResolvedValue(undefined),
  })),
}));

import { JiraHandler } from '../src/integrations/jira/handler.js';
import { AzureBoardsHandler } from '../src/integrations/azure-boards/handler.js';
import { LinearHandler } from '../src/integrations/linear/handler.js';

const mockConfig = {
  github: { token: 'test-token', owner: 'test-owner', repo: 'test-repo' },
  jira: { webhookSecret: '', triggerLabel: 'ai-task' },
  azureBoards: { webhookSecret: '', triggerTag: 'ai-task' },
  linear: { webhookSecret: '', triggerLabel: 'ai-task' },
};

describe('GET /health', () => {
  it('returns 200 with status ok', async () => {
    const app = createServer(mockConfig as never);
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ok');
  });

  it('returns json with timestamp', async () => {
    const app = createServer(mockConfig as never);
    const res = await request(app).get('/health');
    expect(res.body.timestamp).toBeDefined();
    expect(typeof res.body.timestamp).toBe('string');
  });
});

describe('POST /webhooks/jira', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('returns 200 for valid jira:issue_created event', async () => {
    (JiraHandler as jest.MockedClass<typeof JiraHandler>).mockImplementation(
      () =>
        ({
          handle: jest.fn().mockImplementation((_req, res) => {
            res.status(200).json({ message: 'ok' });
            return Promise.resolve();
          }),
        }) as never,
    );

    const app = createServer(mockConfig as never);
    const res = await request(app)
      .post('/webhooks/jira')
      .send({ webhookEvent: 'jira:issue_created' });

    expect(res.status).toBe(200);
  });

  it('handles unknown jira events with 200', async () => {
    (JiraHandler as jest.MockedClass<typeof JiraHandler>).mockImplementation(
      () =>
        ({
          handle: jest.fn().mockImplementation((_req, res) => {
            res.status(200).json({ message: 'Event ignored' });
            return Promise.resolve();
          }),
        }) as never,
    );

    const app = createServer(mockConfig as never);
    const res = await request(app)
      .post('/webhooks/jira')
      .send({ webhookEvent: 'jira:comment_created' });

    expect(res.status).toBe(200);
    expect(res.body.message).toBe('Event ignored');
  });
});

describe('POST /webhooks/azure-boards', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('returns 200 for workitem.created event', async () => {
    (AzureBoardsHandler as jest.MockedClass<typeof AzureBoardsHandler>).mockImplementation(
      () =>
        ({
          handle: jest.fn().mockImplementation((_req, res) => {
            res.status(200).json({ message: 'ok' });
            return Promise.resolve();
          }),
        }) as never,
    );

    const app = createServer(mockConfig as never);
    const res = await request(app)
      .post('/webhooks/azure-boards')
      .send({ eventType: 'workitem.created' });

    expect(res.status).toBe(200);
  });
});

describe('POST /webhooks/linear', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('returns 200 for linear issue create action', async () => {
    (LinearHandler as jest.MockedClass<typeof LinearHandler>).mockImplementation(
      () =>
        ({
          handle: jest.fn().mockImplementation((_req, res) => {
            res.status(200).json({ message: 'ok' });
            return Promise.resolve();
          }),
        }) as never,
    );

    const app = createServer(mockConfig as never);
    const res = await request(app)
      .post('/webhooks/linear')
      .send({ action: 'create', type: 'Issue' });

    expect(res.status).toBe(200);
  });
});

describe('GET /unknown-route', () => {
  it('returns 404', async () => {
    const app = createServer(mockConfig as never);
    const res = await request(app).get('/unknown-route');
    expect(res.status).toBe(404);
  });
});
