package com.crawler.service;

import com.crawler.api.dto.SocialPlatformResponse;
import com.crawler.domain.repository.SocialPlatformRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class SocialPlatformService {

    private final SocialPlatformRepository platformRepository;

    public List<SocialPlatformResponse> findAllPlatforms() {
        return platformRepository.findAll()
                .stream()
                .map(SocialPlatformResponse::from)
                .toList();
    }
}
