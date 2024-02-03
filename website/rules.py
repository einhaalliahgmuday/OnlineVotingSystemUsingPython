from flask_login import current_user
from . import models

def getUser(userId, password, userType):
    user = models.User.query.filter(models.User.userId == userId, models.User.password == password, models.User.userType == userType).first()
    return user

# POST RULES

def getUserPostsCount():
    return models.Post.query.filter(models.Post.userId == current_user.userId).count()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

def getUserPostRole(user):
    if user.userType == "Admin":
        return "Admin"
    else:
        candidate = models.Candidate.query.filter(models.Candidate.studentId == user.userId).first()
        if candidate.position == "president":
            return "President"
        elif candidate.position == "executive_vp":
            return "Executive Vice President"
        elif candidate.position == "executive_board_sec":
            return "Executive Board Secretary"
        elif candidate.position == "vp_finance":
            return "Vice President for Finance"
        elif candidate.position == "vp_academic_affairs":
            return "Vice President for Academic Affairs"
        elif candidate.position == "vp_internal_affairs":
            return "Vice President for Internal Affairs"
        elif candidate.position == "vp_external_affairs":
            return "Vice President for External Affairs"
        elif candidate.position == "vp_public_relations":
            return "Vice President for Public Relations"
        elif candidate.position == "vp_research_dev":
            return "Vice President for Research and Development"
        elif candidate.position == "first_yr_rep":
            return "First Year Representative"
        elif candidate.position == "second_yr_rep":
            return "Second Year Representative"
        elif candidate.position == "third_yr_rep":
            return "Third Year Representative"
        elif candidate.position == "fourth_yr_rep":
            return "Fourth Year Representative"

def getSortedPostsByUserRole():
    order = ["Admin", "President", "Executive Vice President", "Executive Board Secretary", "Vice President for Finance",
             "Vice President for Academic Affairs", "Vice President for Internal Affairs", "Vice President for External Affairs", 
             "Vice President for Public Relations", "Vice President for Research and Development", "First Year Representative",
             "Second Year Representative", "Third Year Representative", "Fourth Year Representative"]

    posts = models.Post.query.all()
    sortedPosts = sorted(posts, key=lambda x: order.index(x.userRole))

    return sortedPosts

# VOTE RULES

def hasVoted():
    voter = models.Vote.query.filter(models.Vote.voter == current_user.userId).first()

    if voter:
        return True
    else:
        return False

def isCandidate():
    isCandidate = False

    for candidate in models.Candidate.query.all():
        if current_user.userId == candidate.studentId:
            isCandidate = True
            break
    
    return isCandidate

def getCandidates():
    candidates = {
        "president": models.Candidate.query.filter_by(position="president").all(),
        "executive_vp": models.Candidate.query.filter_by(position="executive_vp").all(),
        "executive_board_sec": models.Candidate.query.filter_by(position="executive_board_sec").all(),
        "vp_finance": models.Candidate.query.filter_by(position="vp_finance").all(),
        "vp_academic_affairs": models.Candidate.query.filter_by(position="vp_academic_affairs").all(),
        "vp_internal_affairs": models.Candidate.query.filter_by(position="vp_internal_affairs").all(),
        "vp_external_affairs": models.Candidate.query.filter_by(position="vp_external_affairs").all(),
        "vp_public_relations": models.Candidate.query.filter_by(position="vp_public_relations").all(),
        "vp_research_dev": models.Candidate.query.filter_by(position="vp_research_dev").all(),
        "first_yr_rep": models.Candidate.query.filter_by(position="first_yr_rep").all(),
        "second_yr_rep": models.Candidate.query.filter_by(position="second_yr_rep").all(),
        "third_yr_rep": models.Candidate.query.filter_by(position="third_yr_rep").all(),
        "fourth_yr_rep": models.Candidate.query.filter_by(position="fourth_yr_rep").all()
    }
    
    return candidates

def getVoteCount(position, vote):
    voteCount = models.Vote.query.filter(getattr(models.Vote, position) == vote).count()

    return voteCount

def getVotePercentage(position, vote):
    totalVoters = models.Vote.query.count()
    voteCount = getVoteCount(position, vote)
    votePercentage = 0

    if not totalVoters == 0:
        votePercentage = (100 / totalVoters) * voteCount

    return votePercentage

def getAbstainVoteByPosition(position):
    voteCount = getVoteCount(position, "abstain")
    votePercentage = getVotePercentage(position, "abstain")

    return {"position": position, "voteCount": voteCount, "votePercentage": votePercentage}

def serializeCandidateForVoteResults(candidate):
    return {
        'studentId': candidate.studentId,
        'name': candidate.name,
        'position': candidate.position,
        'voteCount': candidate.voteCount,
        'votePercentage': candidate.votePercentage
    }

def getVoteResults():
    totalVoters = models.Vote.query.count()
    voteResults = {"totalVoters": totalVoters,
                  "president": {"candidates": [], "abstain": getAbstainVoteByPosition("president")},
                  "executive_vp": {"candidates": [], "abstain": getAbstainVoteByPosition("executive_vp")},
                  "executive_board_sec": {"candidates": [], "abstain": getAbstainVoteByPosition("executive_board_sec")},
                  "vp_finance": {"candidates": [], "abstain": getAbstainVoteByPosition("vp_finance")},
                  "vp_academic_affairs": {"candidates": [], "abstain": getAbstainVoteByPosition("vp_academic_affairs")},
                  "vp_internal_affairs": {"candidates": [], "abstain": getAbstainVoteByPosition("vp_internal_affairs")},
                  "vp_external_affairs": {"candidates": [], "abstain": getAbstainVoteByPosition("vp_external_affairs")},
                  "vp_public_relations": {"candidates": [], "abstain": getAbstainVoteByPosition("vp_public_relations")},
                  "vp_research_dev": {"candidates": [], "abstain": getAbstainVoteByPosition("vp_research_dev")},
                  "first_yr_rep": {"candidates": [], "abstain": getAbstainVoteByPosition("first_yr_rep")},
                  "second_yr_rep": {"candidates": [], "abstain": getAbstainVoteByPosition("second_yr_rep")},
                  "third_yr_rep": {"candidates": [], "abstain": getAbstainVoteByPosition("third_yr_rep")},
                  "fourth_yr_rep": {"candidates": [], "abstain": getAbstainVoteByPosition("fourth_yr_rep")}}

    dbCandidates = models.Candidate.query.all()
    
    for candidate in dbCandidates:
        if candidate.position == "president":
            candidate.voteCount = getVoteCount(candidate.position, candidate.studentId)
            candidate.votePercentage = getVotePercentage(candidate.position, candidate.studentId)
            voteResults['president']['candidates'].append(serializeCandidateForVoteResults(candidate))
        elif candidate.position == "executive_vp":
            candidate.voteCount = getVoteCount(candidate.position, candidate.studentId)
            candidate.votePercentage = getVotePercentage(candidate.position, candidate.studentId)
            voteResults['executive_vp']['candidates'].append(serializeCandidateForVoteResults(candidate))
        elif candidate.position == "executive_board_sec":
            candidate.voteCount = getVoteCount(candidate.position, candidate.studentId)
            candidate.votePercentage = getVotePercentage(candidate.position, candidate.studentId)
            voteResults['executive_board_sec']['candidates'].append(serializeCandidateForVoteResults(candidate))
        elif candidate.position == "vp_finance":
            candidate.voteCount = getVoteCount(candidate.position, candidate.studentId)
            candidate.votePercentage = getVotePercentage(candidate.position, candidate.studentId)
            voteResults['vp_finance']['candidates'].append(serializeCandidateForVoteResults(candidate))
        elif candidate.position == "vp_academic_affairs":
            candidate.voteCount = getVoteCount(candidate.position, candidate.studentId)
            candidate.votePercentage = getVotePercentage(candidate.position, candidate.studentId)
            voteResults['vp_academic_affairs']['candidates'].append(serializeCandidateForVoteResults(candidate))
        elif candidate.position == "vp_internal_affairs":
            candidate.voteCount = getVoteCount(candidate.position, candidate.studentId)
            candidate.votePercentage = getVotePercentage(candidate.position, candidate.studentId)
            voteResults['vp_internal_affairs']['candidates'].append(serializeCandidateForVoteResults(candidate))
        elif candidate.position == "vp_external_affairs":
            candidate.voteCount = getVoteCount(candidate.position, candidate.studentId)
            candidate.votePercentage = getVotePercentage(candidate.position, candidate.studentId)
            voteResults['vp_external_affairs']['candidates'].append(serializeCandidateForVoteResults(candidate))
        elif candidate.position == "vp_public_relations":
            candidate.voteCount = getVoteCount(candidate.position, candidate.studentId)
            candidate.votePercentage = getVotePercentage(candidate.position, candidate.studentId)
            voteResults['vp_public_relations']['candidates'].append(serializeCandidateForVoteResults(candidate))
        elif candidate.position == "vp_research_dev":
            candidate.voteCount = getVoteCount(candidate.position, candidate.studentId)
            candidate.votePercentage = getVotePercentage(candidate.position, candidate.studentId)
            voteResults['vp_research_dev']['candidates'].append(serializeCandidateForVoteResults(candidate))
        elif candidate.position == "first_yr_rep":
            candidate.voteCount = getVoteCount(candidate.position, candidate.studentId)
            candidate.votePercentage = getVotePercentage(candidate.position, candidate.studentId)
            voteResults['first_yr_rep']['candidates'].append(serializeCandidateForVoteResults(candidate))
        elif candidate.position == "second_yr_rep":
            candidate.voteCount = getVoteCount(candidate.position, candidate.studentId)
            candidate.votePercentage = getVotePercentage(candidate.position, candidate.studentId)
            voteResults['second_yr_rep']['candidates'].append(serializeCandidateForVoteResults(candidate))
        elif candidate.position == "third_yr_rep":
            candidate.voteCount = getVoteCount(candidate.position, candidate.studentId)
            candidate.votePercentage = getVotePercentage(candidate.position, candidate.studentId)
            voteResults['third_yr_rep']['candidates'].append(serializeCandidateForVoteResults(candidate))
        elif candidate.position == "fourth_yr_rep":
            candidate.voteCount = getVoteCount(candidate.position, candidate.studentId)
            candidate.votePercentage = getVotePercentage(candidate.position, candidate.studentId)
            voteResults['fourth_yr_rep']['candidates'].append(serializeCandidateForVoteResults(candidate))
    
    return voteResults

# BALLOT RULES

def getBallotStatus():
    ballot = models.BallotStatus.query.first()
    return ballot.ballotStatus