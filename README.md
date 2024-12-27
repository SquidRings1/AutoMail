# AutoMail

I created this script to help me find an internship or apprenticeship in cybersecurity to validate my year at EPITA. The idea is to take an e-mail list (of recruitment contacts) and run the script to send them an e-mail with a cover letter and CV.
(I'm still looking, that's why I just created it.)

## Installation

### Prerequisites
- Python 3.x

### Installation Steps

```bash
git clone https://github.com/SquidRings1/AutoMail.git
```

```bash
cd AutoMail/
```

```bash
pip install -r requirements.txt
```

To configure the project, rename .env.example to .env and replace all the credentials, then in automail.conf, replace the values. Next, go to the data folder and open recipients.csv and add your email list.

To get gmail application password follow this :
https://knowledge.workspace.google.com/kb/how-to-create-app-passwords-000009237?hl=fr
or you can follow this :
https://itsupport.umd.edu/itsupport?id=kb_article_view&sysparm_article=KB0015112

After this you can simply do :
```bash
python3 main.py
```
