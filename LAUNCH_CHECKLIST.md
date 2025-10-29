# ✅ FARCASTER PREDICTION MARKET - LAUNCH CHECKLIST

**Goal**: All items checked = READY TO LAUNCH

**Estimated Time**: ~30 minutes

---

## 📋 PRE-LAUNCH PHASE (Do First)

### Choose Hosting Provider
- [ ] **Heroku** (Recommended for speed - 5 min)
  - [ ] Created Heroku account
  - [ ] Installed Heroku CLI
  - [ ] Set up git repository
  - [ ] Ready to deploy

- [ ] **Railway** (Alternative - 5 min)
  - [ ] Created Railway account
  - [ ] Connected GitHub
  - [ ] Repository ready
  - [ ] PostgreSQL ready

- [ ] **Docker** (For flexibility)
  - [ ] Docker installed
  - [ ] Hosting provider selected
  - [ ] VPS/droplet created
  - [ ] SSH access ready

- [ ] **Local** (For testing only)
  - [ ] Python 3.8+ installed
  - [ ] Virtual environment ready
  - [ ] Dependencies installed

### Get Required Keys & Configuration
- [ ] **Neynar API Key**
  - [ ] Created account at https://app.neynar.com
  - [ ] Generated API key
  - [ ] Key copied and saved safely
  
- [ ] **Wallet Private Key**
  - [ ] Private key exported from wallet
  - [ ] Never shared or exposed
  - [ ] Stored in .env (never in code)
  
- [ ] **RPC Endpoint**
  - [ ] Selected network (Base recommended)
  - [ ] RPC endpoint saved
  - [ ] Endpoint tested (optional)

- [ ] **Treasure Wallet**
  - [ ] Address confirmed: `0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC`
  - [ ] Wallet funded with 1-5 ETH
  - [ ] Balance verified on block explorer

---

## 🔧 CONFIGURATION PHASE

### Environment Variables
- [ ] Created `.env` file from `.env.example`
- [ ] `FLASK_ENV` set to `production`
- [ ] `SECRET_KEY` set to random 32+ character string
- [ ] `NEYNAR_API_KEY` configured
- [ ] `WALLET_PRIVATE_KEY` configured
- [ ] `RPC_ENDPOINT` configured
- [ ] `TREASURE_WALLET` configured (0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC)
- [ ] `DATABASE_URL` configured for production
- [ ] `.env` added to `.gitignore`
- [ ] `.env` NOT committed to Git

### Database Configuration
- [ ] **For Heroku**:
  - [ ] PostgreSQL addon created: `heroku addons:create heroku-postgresql:hobby-dev`
  - [ ] DATABASE_URL auto-set by Heroku

- [ ] **For Railway**:
  - [ ] PostgreSQL database created in dashboard
  - [ ] DATABASE_URL copied to variables

- [ ] **For Docker/Local**:
  - [ ] PostgreSQL installed/running
  - [ ] Database created: `prediction_market`
  - [ ] User created with credentials
  - [ ] DATABASE_URL configured

### Code Updates (if needed)
- [ ] Verified TREASURE_WALLET is correct in `project.py` (line 25)
- [ ] Verified BASE_FEE is $0.20 in `project.py` (line 26)
- [ ] Verified WIN_FEE_PERCENTAGE is 1.5% in `project.py` (line 27)
- [ ] Updated API_BASE_URL with production domain
- [ ] Updated FRAME_URL with production domain
- [ ] No hardcoded secrets in code

---

## 🚀 DEPLOYMENT PHASE

### Heroku Deployment (if chosen)
- [ ] Git repository ready
- [ ] `Procfile` present in root directory
- [ ] `requirements.txt` updated with gunicorn
- [ ] Logged in to Heroku CLI: `heroku login`
- [ ] Created app: `heroku create your-app-name`
- [ ] Environment variables set via Heroku dashboard or CLI
- [ ] PostgreSQL addon created
- [ ] Deployed code: `git push heroku main`
- [ ] Check deployment: `heroku logs --tail`
- [ ] App status: `heroku ps`

### Railway Deployment (if chosen)
- [ ] Connected GitHub repository
- [ ] Railway auto-detected Python app
- [ ] PostgreSQL database created
- [ ] Environment variables configured in dashboard
- [ ] Deployment triggered (auto on GitHub push)
- [ ] Verified build success
- [ ] App URL shown in dashboard

### Docker Deployment (if chosen)
- [ ] `Dockerfile` reviewed and ready
- [ ] `docker-compose.yml` configured
- [ ] `.env` file created with all variables
- [ ] Local test successful: `docker-compose up -d`
- [ ] Health check passed: `curl http://localhost:5000/api/health`
- [ ] Pushed to production server
- [ ] Docker containers running on server
- [ ] Nginx reverse proxy configured (optional)
- [ ] SSL certificate installed (if needed)

### Local Deployment (testing only)
- [ ] Virtual environment activated
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` file created
- [ ] Database initialized
- [ ] Server running: `python main.py`
- [ ] Accessible at `http://localhost:5000`

---

## 🧪 TESTING PHASE

### Basic Health Checks
- [ ] Server is running and accessible
- [ ] Health endpoint responds: `GET /api/health`
- [ ] Response status: 200
- [ ] Response includes: `{"status": "ok"}`

### API Endpoint Tests
- [ ] Markets endpoint working: `GET /api/markets`
- [ ] Create market endpoint: `POST /api/markets/create`
- [ ] Bet placement endpoint: `POST /api/bets/place`
- [ ] User profile endpoint: `GET /api/users/{fid}`
- [ ] Market settlement: `POST /api/markets/{id}/settle`
- [ ] Withdrawal endpoint: `POST /api/withdrawals/request`

### Fee System Tests
- [ ] Base fee ($0.20) charged on bet placement
- [ ] Test transaction shows correct total: bet_amount + $0.20
- [ ] Win fee (1.5%) calculated on winnings
- [ ] Fees routed to treasure wallet
- [ ] Treasure wallet balance increased
- [ ] Fee tracking in database correct

### Database Tests
- [ ] Database connection successful
- [ ] Tables created properly
- [ ] Data persists between restarts
- [ ] User data saved
- [ ] Market data saved
- [ ] Bet data saved
- [ ] Transaction history saved

### Wallet Tests
- [ ] Treasure wallet has funds (1-5 ETH)
- [ ] Transactions can be sent from wallet
- [ ] Transaction fees paid from wallet
- [ ] Wallet balance updated correctly
- [ ] Transaction hashes recorded
- [ ] Block explorer shows transactions

---

## 🌐 DOMAIN & SSL SETUP

### Custom Domain (Optional but Recommended)
- [ ] Domain name purchased/registered
- [ ] Domain pointed to your hosting provider
- [ ] DNS records updated:
  - [ ] A record or CNAME configured
  - [ ] DNS propagated (wait 5-30 minutes)
  - [ ] Domain resolves to app: `nslookup your-domain.com`

### SSL Certificate
- [ ] SSL certificate obtained:
  - [ ] Heroku: auto-provided
  - [ ] Railway: auto-provided
  - [ ] Docker/DigitalOcean: Let's Encrypt installed
- [ ] HTTPS accessible: `https://your-domain.com`
- [ ] Certificate valid and not expired
- [ ] Browser shows secure connection

### CORS Configuration
- [ ] CORS enabled for production domain
- [ ] Allowed origins configured
- [ ] Preflight requests handled
- [ ] Cross-origin requests work

---

## 🎭 FARCASTER INTEGRATION (Optional)

### Signer Registration
- [ ] Signer created via Neynar API
- [ ] Signer UUID obtained
- [ ] Signer UUID added to `.env`
- [ ] Frame endpoint available: `GET /frame`

### Frame Setup
- [ ] Frame URL configured in code
- [ ] Frame endpoint responsive
- [ ] Frame renders in Farcaster client
- [ ] Buttons clickable
- [ ] Frame interactions work

### Profile Integration
- [ ] Farcaster profile updated with frame URL
- [ ] Bio includes link to prediction market
- [ ] Profile visible to public
- [ ] Others can access frame from profile

---

## 📊 MONITORING & ALERTS

### Error Tracking
- [ ] Error tracking service configured (optional)
  - [ ] Sentry account created (if using)
  - [ ] Sentry DSN configured
  - [ ] Errors being captured
  - [ ] Alert emails configured

### Logging
- [ ] Log files created: `logs/app.log`
- [ ] Logs being written to file
- [ ] Log rotation configured
- [ ] Important events logged:
  - [ ] Bets placed
  - [ ] Markets settled
  - [ ] Withdrawals processed
  - [ ] Errors captured

### Monitoring Dashboards
- [ ] Uptime monitoring configured (optional)
  - [ ] Uptime Robot account created
  - [ ] Health check endpoint monitored
  - [ ] Alerts set up for downtime
  - [ ] Status page accessible

- [ ] Performance monitoring (optional)
  - [ ] Response time tracking
  - [ ] Database query monitoring
  - [ ] API endpoint metrics
  - [ ] Error rate tracking

---

## 🔒 SECURITY CHECKLIST

### Secrets Management
- [ ] Private keys NOT in Git
- [ ] API keys NOT in source code
- [ ] `.env` in `.gitignore`
- [ ] Secrets stored in environment only
- [ ] Production uses secure secret storage

### API Security
- [ ] Input validation enabled
- [ ] SQL injection protection enabled
- [ ] Rate limiting configured
- [ ] CORS properly restricted
- [ ] HTTPS enforced (in production)
- [ ] Error messages don't expose sensitive info

### Database Security
- [ ] Database password is strong
- [ ] Database user has limited permissions
- [ ] SSL connection to database (if remote)
- [ ] Backups configured
- [ ] Backup tested and verified

### Wallet Security
- [ ] Private key stored securely
- [ ] Private key never logged
- [ ] Private key never in error messages
- [ ] Wallet transactions verified
- [ ] Transaction signatures correct

---

## 📈 PERFORMANCE VERIFICATION

### Response Time Tests
- [ ] Health check: < 100ms
- [ ] Market list: < 200ms
- [ ] Create market: < 300ms
- [ ] Place bet: < 300ms
- [ ] Get user: < 200ms
- [ ] Settle market: < 500ms

### Load Tests (Optional)
- [ ] Can handle 100 requests/minute
- [ ] Can handle 1000 concurrent users
- [ ] No memory leaks detected
- [ ] Database connections stable

### Scalability
- [ ] Can upgrade resources if needed
- [ ] Horizontal scaling possible
- [ ] Auto-scaling configured (if available)
- [ ] Database can handle growth

---

## 📝 DOCUMENTATION

### User Documentation
- [ ] User guide created
- [ ] API documentation complete
- [ ] Examples provided
- [ ] FAQ written
- [ ] Help system in place

### Developer Documentation
- [ ] Code comments clear
- [ ] API endpoints documented
- [ ] Database schema documented
- [ ] Configuration options documented
- [ ] Deployment instructions included

### Operations Documentation
- [ ] Deployment procedure documented
- [ ] Monitoring setup documented
- [ ] Backup/restore procedure documented
- [ ] Troubleshooting guide created
- [ ] On-call procedures defined

---

## 🎯 FINAL VERIFICATION

### Before Announcement
- [ ] All above items checked
- [ ] No known bugs or issues
- [ ] System tested end-to-end
- [ ] Team verified everything works
- [ ] Wallet funded and ready
- [ ] Monitoring active
- [ ] Support team ready

### Go-Live Checklist
- [ ] Announcement prepared
- [ ] Social media posts ready
- [ ] Farcaster posts prepared
- [ ] Team notified of launch time
- [ ] Monitoring setup and active
- [ ] Support team on standby
- [ ] Backup plan in case of issues

### Post-Launch
- [ ] Monitor closely for first 24 hours
- [ ] Check logs regularly
- [ ] Monitor wallet balance
- [ ] Gather user feedback
- [ ] Fix any issues immediately
- [ ] Celebrate! 🎉

---

## 🆘 TROUBLESHOOTING REFERENCE

If something goes wrong, check here:

| Problem | Solution |
|---------|----------|
| **502 Bad Gateway** | Check database is connected, check logs |
| **500 Internal Error** | Check environment variables, check logs |
| **Can't connect to wallet** | Check private key format, check RPC endpoint |
| **Fees not collected** | Check treasure wallet address, check gas |
| **Database connection fails** | Check DATABASE_URL, check credentials |
| **Slow response times** | Check database queries, upgrade resources |
| **Can't access via domain** | Check DNS records, check SSL cert |
| **Frame not showing in Farcaster** | Check frame URL, test endpoint directly |

---

## ✨ LAUNCH SUCCESS CRITERIA

Your launch is successful when:

```
✅ Server is running and accessible
✅ All API endpoints responding (< 300ms)
✅ Database connected and working
✅ Fees being collected to treasure wallet
✅ Users can create bets
✅ Users can withdraw winnings
✅ Monitoring active and alerting
✅ Documentation complete
✅ Team notified and ready for support
✅ First users onboarded successfully
```

---

## 📞 FINAL CHECKS

- [ ] Share this checklist with your team
- [ ] Assign ownership for each section
- [ ] Set timeline for completion
- [ ] Schedule launch meeting
- [ ] Prepare status updates

---

## 🎊 YOU'RE READY TO LAUNCH!

**Print this checklist and use it as your launch guide.**

**Time to completion: ~30 minutes**

**Status: READY FOR PRODUCTION**

---

### Quick Reference URLs

**Key Files:**
- Deployment Guide: `PRODUCTION_DEPLOYMENT_GUIDE.md`
- Quick Launch: `QUICK_LAUNCH_GUIDE.md`
- Start Here: `START_HERE_DEPLOYMENT.md`
- Complete Index: `INDEX.md`

**External Links:**
- Heroku: https://www.heroku.com
- Railway: https://railway.app
- Neynar: https://app.neynar.com
- Treasure Wallet: https://basescan.org/address/0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC

---

**Good luck with your launch! 🚀**