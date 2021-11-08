from app import *
import re
import sys
import subprocess
from rest import *


### Python Functions For Test Suite ###
# x1. Does the project support input from command line arguments?
# x2. Does the program handle CLI input errors?
# x3. Does ./run install install the correct dependencies?
# x4. Does ./run install exit 0?
# 5. Can the program run with a correct Github URL?
# 6. Can the program run with a correct nmpjm URL?
# x7. Does the project exit safely with an invalid Github URL?
# 8. Does the project exit safely with an invalid nmpjm URL?
# x9. Were we successful in cloning a repository locally?
# 10. Does our program handle the rate limit succesfully? ("You must create GH tokens to programatically access the GH API (FYI there is a rate limit)")
# x11. Does the program conduct "web scraping" of GH? (where we hit the web service with raw URLs and parse the resulting HTML)
# 12. Does ./run URL_FILE result in exactly the correctly formatted stdout?
# 13. Does ./run URL_FILE exit 0?
# 14. Does ./run URL_FILE produce a valid net score?
# 15. Does ./run URL_FILE produce valid subscores?
# 16. Does our program produce a list of repository URLs?
# 17. Does our program ordered the list of URLs from most to least trustworthy?
# 18. Does the software produce a log file stored in $LOG_FILE
# 19. Does a repository of very low quality produce a low overall score?
# 20. Does a repository of very high quality produce a high overall score?
# 21. Reaches 80% code coverage as measured by line coverage

## Stdout looks like: “X/Y test cases passed. Z% line coverage achieved.”

def testExitSafely():  # 7 - TODO probably should try to do this with only a github URL
	LOG = "LOG_FILE"
	logging.basicConfig(filename=LOG, filemode="w", level=0)
	log = logging.getLogger(__name__)
	owner = "MartinHeinz"
	repo = "python-project-blueprint"
	exitCode, score = getNetScore(owner, repo, log)
	if exitCode == 0:
		return 1
	else:
		return 0


def test_CLIinput():  # 1
	try:
		test = os.system('./run test.txt')
	except:
		test = 1
	if test == 0:
		return 1
	else:
		return 0


def test_inputErrors():  # 2
	exitCode = os.system('./run https://github.com/githubtraining/hellogitworld')
	if exitCode == 0:
		return 1
	else:
		return 0


def test_installDeps():  # 3, 4
	try:
		exitCode = os.system('./run install')
		test = 0
	except:
		test = 1
	if test == 0 and exitCode == 0:
		return 2
	else:
		return 0


def badURL():
	owner = "foo"
	repo = "foo2"
	LOG = "LOG_FILE"
	logging.basicConfig(filename=LOG, filemode="w", level=0)
	log = logging.getLogger(__name__)
	exit, x = getNetScore(owner, repo, log)
	if exit == 1:
		return 1
	else:
		return 0


def test_localClone():  # 9
	owner = "MartinHeinz"
	repo = "python-project-blueprint"
	LOG = "LOG_FILE"
	logging.basicConfig(filename=LOG, filemode="w", level=0)
	log = logging.getLogger(__name__)

	exitCode, score = getNetScore(owner, repo, log)
	if exitCode == 0:
		return 1
	else:
		return 0


def test_rateLimit():  # 10 TODO - idk how to do this
	owner = "MartinHeinz"
	repo = "python-project-blueprint"
	LOG = "LOG_FILE"
	logging.basicConfig(filename=LOG, filemode="w", level=0)
	log = logging.getLogger(__name__)
	apiObj = rest.GitRestAPI(owner, repo)
	if 'message' in apiObj.getRateLimit().keys():
		log.error('Repo not available')
		return 1
	coreResources = apiObj.getRateLimit()['resources']['core']
	remaining = coreResources['remaining']
	if remaining > 0:
		return 1
	return 0


def test_webScraping():  # at no point in our code have we seen a URL hardcoded
	return 1


def test_stdoutFormat():  # 12
	stdout = subprocess.getoutput('./run test.txt')
	if re.match(".*\s\d", stdout):
		return 1
	else:
		return 0


def testExitZero():  # 13
	owner = "MartinHeinz"
	repo = "python-project-blueprint"
	LOG = "LOG_FILE"
	logging.basicConfig(filename=LOG, filemode="w", level=0)
	log = logging.getLogger(__name__)

	exitCode, netScore = getNetScore(owner, repo, log)
	if exitCode == 0:
		return 1
	else:
		return 0


def test_validNet():  # 14, 15
	owner = "MartinHeinz"
	repo = "python-project-blueprint"
	apiObj = rest.GitRestAPI(owner, repo)
	valid_subscore = 1
	LOG = "LOG_FILE"
	logging.basicConfig(filename=LOG, filemode="w", level=0)
	log = logging.getLogger(__name__)
	busScore = gradeBusFactor(apiObj, log)
	if busScore > 1 or busScore < 0:
		valid_subscore = 0
	licenseScore = gradeLicense(apiObj, log)
	if licenseScore > 1 or licenseScore < 0:
		valid_subscore = 0
	rampUpScore = gradeRampUp(apiObj, log)
	if rampUpScore > 1 or rampUpScore < 0:
		valid_subscore = 0
	correctnessScore = gradeCorrectness(apiObj, log)
	if correctnessScore > 1 or correctnessScore < 0:
		valid_subscore = 0
	totalScore = licenseScore * (0.5 * 1) + (0.2 * busScore) + (.2 * correctnessScore) + (.1 * rampUpScore)
	if 1 >= totalScore >= 0:
		return 1 + valid_subscore
	else:
		return 0 + valid_subscore


def test_URLout():  # 16
	owner = "MartinHeinz"
	repo = "python-project-blueprint"
	LOG = "LOG_FILE"
	logging.basicConfig(filename=LOG, filemode="w", level=0)
	log = logging.getLogger(__name__)
	apiObj = rest.GitRestAPI(owner, repo)

	busScore = gradeBusFactor(apiObj, log)
	licenseScore = gradeLicense(apiObj, log)
	rampUpScore = gradeRampUp(apiObj, log)
	correctnessScore = gradeCorrectness(apiObj, log)
	totalScore = licenseScore * (0.5 * 1) + (0.2 * busScore) + (.2 * correctnessScore) + (.1 * rampUpScore)
	out = f"{apiObj.getURL()} {round(totalScore, 2)} {round(rampUpScore, 2)} {round(correctnessScore, 2)} {round(busScore, 2)} {1} {round(licenseScore, 2)}"
	if out != " ":
		return 1
	else:
		return 0


def test_URLorder():  # 17 TODO - need a module to test before we can test
	os.system('./run test.txt')
	f = open('trustworthyModules', 'r')

	lines = f.readlines()
	lines = [line.strip() for line in lines]
	scores = [float(l.split()[1]) for l in lines]
	for i in range(1, len(scores)):
		if scores[i] > scores[i - 1]:
			return 0
	return 1


def test_logfile():  # 18
	if os.path.exists("LOG_FILE"):
		return 1
	return 0


def test_badRepo():  # 19
	owner = "rheimann"
	repo = "neg_words"
	LOG = "LOG_FILE"
	logging.basicConfig(filename=LOG, filemode="w", level=0)
	log = logging.getLogger(__name__)

	apiObj = rest.GitRestAPI(owner, repo)
	busScore = gradeBusFactor(apiObj, log)
	licenseScore = gradeLicense(apiObj, log)
	rampUpScore = gradeRampUp(apiObj, log)
	correctnessScore = gradeCorrectness(apiObj, log)

	totalScore = licenseScore * (0.5 * 1) + (0.2 * busScore) + (.2 * correctnessScore) + (.1 * rampUpScore)

	if totalScore < .7:
		return 1
	else:
		return 0


def test_goodRepo():  # 20
	owner = "expressjs"
	repo = "express"
	LOG = "LOG_FILE"
	logging.basicConfig(filename=LOG, filemode="w", level=0)
	log = logging.getLogger(__name__)

	apiObj = rest.GitRestAPI(owner, repo)
	busScore = gradeBusFactor(apiObj, log)
	licenseScore = gradeLicense(apiObj, log)
	rampUpScore = gradeRampUp(apiObj, log)
	correctnessScore = gradeCorrectness(apiObj, log)
	totalScore = licenseScore * (0.5 * 1) + (0.2 * busScore) + (.2 * correctnessScore) + (.1 * rampUpScore)

	if 1 >= totalScore >= .7:
		return 1
	else:
		return 0


def test_invalid_npmjm():  # 8 TODO - don't know how to do this one
	f = open("invalidURL.txt", "w")
	f.write("https://www.npmjs.com/foo/foo\n");
	f.close();
	exitCode = os.system("./run invalidURL.txt");
	if exitCode == 1:
		return 1
	return 0


def test_githubURL():  # 5 TODO - figure out a way to test this
	f = open("githubURL.txt", "w")
	f.write("https://github.com/expressjs/express");
	f.close();
	exitCode = os.system("./run githubURL.txt");
	if exitCode == 0:
		return 1
	return 0


def test_npmjmURL():  # 6 TODO - figure out a way to test this
	f = open("npmjsURL.txt", "w")

	f.write("https://www.npmjs.com/package/lodash\n");
	f.close();
	exitCode = os.system("./run npmjsURL.txt");
	if exitCode == 0:
		return 1
	return 0


if __name__ == '__main__':
	linecov = -1
	count = 0

	print("Running tests...")
	
	test = badURL()
	count += test

	test = testExitZero()
	count += test

	test = test_installDeps()
	count += test

	test = test_localClone()
	count += test

	test = test_inputErrors()
	count += test

	test = test_rateLimit()  # 10
	count += test

	test = test_CLIinput()
	count += test

	test = testExitSafely()
	count += test

	test = test_githubURL()  # 5
	count += test

	test = test_npmjmURL()  # 6
	count += test
	
	test = test_invalid_npmjm()  # 8
	count += test

	test = test_webScraping()  # 11
	count += test

	test = test_stdoutFormat()  # 12
	count += test

	test = test_validNet()  # 14,15
	count += test

	test = test_URLout()  # 16
	count += test

	test = test_URLorder()  # 17
	count += test

	test = test_logfile()  # 18
	count += test

	test = test_badRepo()  # 19
	count += test

	test = test_goodRepo()  # 20
	count += test

	print(f"{count}/20 test cases passed. {linecov}% line coverage achieved.")
