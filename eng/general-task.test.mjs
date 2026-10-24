import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { runInNewContext } from 'node:vm'
import test from 'node:test'

const source = readFileSync(new URL('../MediaCleaner/Web/general.js', import.meta.url), 'utf8')
    .replace('export default function (view, params)', 'function initializeGeneralPage(view, params)')

test('cleanup task lookup awaits Jellyfin response parsing and enables the run button', async () => {
    const requests = []
    const task = { Id: 'task-123', Key: 'MediaCleanup', State: 'Idle', Triggers: [] }
    const context = {
        ApiClient: {
            getUrl: path => path,
            fetch: async request => {
                requests.push(request)
                return { json: async () => [{ Id: 'other-task', Key: 'Other' }, task] }
            },
        },
    }
    runInNewContext(source, context)

    const found = await context.getCleanupTask()
    assert.equal(found.Id, task.Id)
    assert.equal(requests.length, 1)
    assert.equal(requests[0].url, 'ScheduledTasks')
    assert.equal(requests[0].type, 'GET')

    const button = { disabled: true }
    context.updateRunNowButton({
        _mediaCleanerTask: found,
        querySelector: selector => {
            assert.equal(selector, '#MediaCleanerRunNow')
            return button
        },
    })
    assert.equal(button.disabled, false)
})
