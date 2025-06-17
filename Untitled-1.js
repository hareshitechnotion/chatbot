const eventData = $input.first();

// Check if we have valid webhook data
if (!eventData || !eventData.json) {
  return {
    json: {
      error: "Invalid webhook data received",
      received_data: eventData
    }
  };
}

// Extract PR information
const pr = eventData.json.body?.pull_request || {};
const repo = eventData.json.body?.repository || {};

// Prepare the basic response
const result = {
  event_type: eventData.json.headers?.['x-github-event'] || "unknown",
  action: eventData.json.body?.action || "unknown",
  repository: {
    name: repo.name || "unknown",
    full_name: repo.full_name || "unknown",
    owner: repo.owner?.login || "unknown"
  },
  pull_request: {
    number: pr.number || null,
    title: pr.title || "No title",
    html_url: pr.html_url || null,
    state: pr.state || "unknown"
  },
  timestamp: new Date().toISOString()
};

// Get the diff directly from GitHub
if (pr.diff_url) {
  try {
    // Method 1: Get the unified diff (recommended)
    const diffResponse = await fetch(pr.diff_url);
    const diffText = await diffResponse.text();
    
    // Method 2: Alternatively, get structured file changes
    const filesResponse = await fetch(`${pr.url}/files`);
    const filesData = await filesResponse.json();
    
    result.diff = {
      raw_diff: diffText.length > 1000 ? 
        diffText.substring(0, 1000) + "... (truncated)" : 
        diffText,
      files: Array.isArray(filesData) ? filesData.map(file => ({
        filename: file.filename,
        status: file.status,
        additions: file.additions,
        deletions: file.deletions,
        changes: file.changes,
        patch: file.patch || "View full diff at PR URL"
      })) : []
    };
    
  } catch (error) {
    result.diff_error = {
      message: "Failed to fetch diff details",
      details: error.message,
      fallback_urls: {
        diff_url: pr.diff_url,
        patch_url: pr.patch_url
      }
    };
  }
} else {
  result.diff_error = "No diff URL available in PR data";
}

return {
  json: result
};