package com.crawler.api.dto;

import com.crawler.domain.entity.SocialPostCrawl;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;

@Getter
@Builder
public class SocialPostCrawlResponse {

    private Long spcId;
    private String platformId;
    private String crawlCase;
    private String brandName;
    private String accountId;
    private String accountType;
    private String postId;
    private String postUrl;
    private String postType;
    private LocalDateTime postedAt;
    private String postTitle;
    private String textContent;
    private String personTags;
    private String hashtags;
    private String mediaUrl;
    private String thumbnailUrl;
    private Long viewCount;
    private Long likeCount;
    private Long commentCount;
    private Long shareCount;
    private String authorName;
    private Long authorFollowers;
    private boolean duplicate;
    private boolean junk;
    private LocalDateTime createdAt;

    public static SocialPostCrawlResponse from(SocialPostCrawl post) {
        return SocialPostCrawlResponse.builder()
                .spcId(post.getSpcId())
                .platformId(post.getPlatformId())
                .crawlCase(post.getCrawlCase())
                .brandName(post.getBrandName())
                .accountId(post.getAccountId())
                .accountType(post.getAccountType())
                .postId(post.getPostId())
                .postUrl(post.getPostUrl())
                .postType(post.getPostType())
                .postedAt(post.getPostedAt())
                .postTitle(post.getPostTitle())
                .textContent(post.getTextContent())
                .personTags(post.getPersonTags())
                .hashtags(post.getHashtags())
                .mediaUrl(post.getMediaUrl())
                .thumbnailUrl(post.getThumbnailUrl())
                .viewCount(post.getViewCount())
                .likeCount(post.getLikeCount())
                .commentCount(post.getCommentCount())
                .shareCount(post.getShareCount())
                .authorName(post.getAuthorName())
                .authorFollowers(post.getAuthorFollowers())
                .duplicate(post.isDuplicate())
                .junk(post.isJunk())
                .createdAt(post.getCreatedAt())
                .build();
    }
}