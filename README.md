# Driveline Website

Official website for [Driveline](https://devdismissal.github.io/website) — School dismissal and family check-in platform.

## Pages

| File | Description |
|---|---|
| `index.html` | Main landing page |
| `privacy.html` | Privacy Policy |

## About

Driveline streamlines school dismissal with secure family check-in, parent notifications, and staff handoff records. Built for safety, designed for simplicity.

## Features

- **Family Check-In:** Separate adult accounts with per-child pickup claims
- **Real-Time Notifications:** Instant SMS and email alerts for parents
- **Staff Handoff Records:** Complete audit trail of pickups
- **Permission Scoping:** Role-based access control
- **Near-School Detection:** GPS-based proximity verification
- **Open Source:** Self-hostable and fully transparent

## Development

This is a static GitHub Pages site. To run locally:

```bash
# Serve the site locally (requires Python 3)
python3 -m http.server 8000

# Or use any static file server
npx serve .
```

Visit `http://localhost:8000` in your browser.

## Deployment

This site is automatically deployed to GitHub Pages when pushed to the `main` branch.

## Contributing

This is the public website repository for Driveline. For issues or suggestions related to the website, please open a GitHub issue.

For the main application code, see [AgenticEHR/DrivelineDismissal](https://github.com/AgenticEHR/DrivelineDismissal).

## License

MIT License - see the main [Driveline repository](https://github.com/AgenticEHR/DrivelineDismissal) for details.

## Legal

© 2026 Driveline. All rights reserved.
