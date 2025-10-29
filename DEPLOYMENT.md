# Deployment Guide - Farcaster Prediction Market

## 📦 Deployment Options

### Option 1: Heroku (Easiest)

#### Prerequisites
- Heroku account
- Heroku CLI installed

#### Steps

1. **Create Heroku app**
```bash
heroku create your-app-name
```

2. **Add PostgreSQL addon**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

3. **Set environment variables**
```bash
heroku config:set NEYNAR_API_KEY=your_key
heroku config:set ALCHEMY_RPC_URL=your_url
heroku config:set PRIVATE_KEY=your_key
heroku config:set FLASK_ENV=production
```

4. **Deploy**
```bash
git push heroku main
```

5. **Initialize database**
```bash
heroku run python -c "from project import app; from database import init_db; app_context = app.app_context(); app_context.push(); init_db(app)"
```

6. **Access your app**
```
https://your-app-name.herokuapp.com
```

### Option 2: Docker on DigitalOcean / AWS

#### Prerequisites
- Docker and Docker Compose installed
- DigitalOcean/AWS account
- Domain name (optional)

#### Build Docker Image

1. **Build locally**
```bash
docker build -t prediction-market:latest .
```

2. **Test locally**
```bash
docker run -p 5000:5000 --env-file .env prediction-market:latest
```

#### Deploy to DigitalOcean App Platform

1. **Push to Docker Hub**
```bash
docker tag prediction-market:latest yourusername/prediction-market:latest
docker push yourusername/prediction-market:latest
```

2. **Create DigitalOcean App**
   - Go to DigitalOcean App Platform
   - Select "Create App"
   - Choose Docker Hub repository
   - Configure environment variables
   - Deploy

#### Deploy with Docker Compose on VPS

1. **SSH into VPS**
```bash
ssh root@your-vps-ip
```

2. **Clone repository**
```bash
git clone https://github.com/yourusername/farcaster-prediction-market.git
cd farcaster-prediction-market
```

3. **Create .env file**
```bash
nano .env
# Add your configuration
```

4. **Start services**
```bash
docker-compose up -d
```

5. **Check status**
```bash
docker-compose logs -f web
```

### Option 3: Railway

#### Steps

1. **Connect GitHub repository**
   - Go to railway.app
   - Click "New Project"
   - Select your GitHub repo

2. **Add PostgreSQL service**
   - Add plugin: PostgreSQL
   - Railway auto-links to app

3. **Set environment variables**
   - Go to Variables tab
   - Add your keys

4. **Deploy**
   - Railway auto-deploys on git push

### Option 4: AWS Lambda + RDS

#### Architecture
- AWS Lambda: API endpoints
- AWS RDS: PostgreSQL database
- AWS S3: File storage
- CloudFront: CDN

#### Deployment Steps

1. **Create RDS instance**
```bash
aws rds create-db-instance \
  --db-instance-identifier prediction-market-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --allocated-storage 20
```

2. **Install Serverless Framework**
```bash
npm install -g serverless
```

3. **Deploy**
```bash
serverless deploy
```

4. **Configure API Gateway**
   - Create API Gateway
   - Link to Lambda functions

## 🔒 Production Checklist

### Security
- [ ] Enable SSL/TLS certificate
- [ ] Set `FLASK_ENV=production`
- [ ] Update `SECRET_KEY` with random value
- [ ] Enable CSRF protection
- [ ] Setup rate limiting
- [ ] Enable CORS only for trusted origins
- [ ] Use environment variables for secrets
- [ ] Enable database backups

### Performance
- [ ] Setup Redis cache
- [ ] Enable gzip compression
- [ ] Configure CDN
- [ ] Setup database connection pooling
- [ ] Enable query result caching
- [ ] Setup monitoring/alerts

### Operations
- [ ] Setup error tracking (Sentry)
- [ ] Setup logging (ELK stack)
- [ ] Setup monitoring (Datadog/New Relic)
- [ ] Setup automated backups
- [ ] Create deployment runbook
- [ ] Setup CI/CD pipeline

### Database
- [ ] Migrate from SQLite to PostgreSQL
- [ ] Setup database replication
- [ ] Enable automated backups
- [ ] Configure connection pooling

## 🚀 CI/CD with GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Login to DockerHub
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push
        uses: docker/build-push-action@v2
        with:
          context: .
          push: true
          tags: yourusername/prediction-market:latest
      
      - name: Deploy to production
        uses: actions/ssh-remote-commands@v1
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd /app/farcaster-prediction-market
            git pull origin main
            docker-compose pull
            docker-compose up -d
```

## 📊 Monitoring & Logging

### Setup Sentry for error tracking

1. **Install Sentry**
```bash
pip install sentry-sdk[flask]
```

2. **Configure in main.py**
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()]
)
```

### Setup CloudWatch (AWS)

1. **Install logging**
```bash
pip install watchtower
```

2. **Configure logging**
```python
import watchtower
import logging

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        watchtower.CloudWatchLogHandler()
    ]
)
```

## 🔄 Database Migrations

### Initial Migration
```bash
# Export from SQLite to PostgreSQL
pg_dump -U postgres prediction_market > dump.sql
psql -U postgres -d production_market < dump.sql
```

### Backup Strategy

Daily backups:
```bash
0 2 * * * /usr/local/bin/backup-db.sh
```

Backup script (`backup-db.sh`):
```bash
#!/bin/bash
DATE=$(date +%Y-%m-%d)
pg_dump prediction_market > /backups/prediction_market_$DATE.sql
gzip /backups/prediction_market_$DATE.sql
aws s3 cp /backups/prediction_market_$DATE.sql.gz s3://backups/
```

## 🔐 SSL/TLS Configuration

### Using Let's Encrypt

1. **Install Certbot**
```bash
sudo apt-get install certbot python3-certbot-nginx
```

2. **Obtain certificate**
```bash
sudo certbot certonly --nginx -d your-domain.com
```

3. **Configure Nginx**
```nginx
ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
```

4. **Auto-renewal**
```bash
sudo certbot renew --dry-run
```

## 📈 Scaling

### Horizontal Scaling (Multiple instances)

1. **Load Balancer**
   - Use Nginx, HAProxy, or cloud LB

2. **Session Management**
   - Store sessions in Redis
   - Configure in Flask

3. **Database**
   - Setup read replicas
   - Enable connection pooling

### Vertical Scaling

- Increase server CPU/RAM
- Upgrade database tier
- Enable caching layers

## 🧪 Testing Deployment

### Smoke Tests
```bash
curl https://your-domain.com/health
```

### API Tests
```bash
python tests/test_api.py --url https://your-domain.com
```

### Load Testing
```bash
# Using locust
locust -f tests/load_test.py --host=https://your-domain.com
```

## 📝 Runbook Template

### Deployment Steps

1. Code review and merge to main
2. Run test suite
3. Build Docker image
4. Push to registry
5. Deploy to staging
6. Run smoke tests
7. Deploy to production
8. Monitor logs

### Rollback Procedure

```bash
# Get previous version
docker pull prediction-market:previous

# Rollback
docker-compose stop web
docker-compose up -d web
```

## 🆘 Troubleshooting Deployment

### Container won't start
```bash
docker logs prediction-market-web
# Check configuration and logs
```

### Database connection error
```bash
# Check connection string
echo $DATABASE_URL
# Verify database is running
docker-compose logs db
```

### High memory usage
```bash
# Check processes
docker stats
# Optimize app code or increase resources
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Flask Deployment](https://flask.palletsprojects.com/deployment/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)

---

For questions, check GitHub Issues or contact support.